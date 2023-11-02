import aiohttp
import asyncio
import logging

from pathlib import Path
from typing import List, Optional

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
from langchain.text_splitter import TextSplitter

from .models import Page, PageListItem

logger = logging.getLogger(__name__)


def _get_session(url: str, token: str):
    """
    Generate aiohttp session with authentication headers

    Args:
        url: GraphQL endpoint url
        token: Authentication token
    """

    # Build headers
    headers = {"Authorization": f"Bearer {token}"}

    # Create session
    session = aiohttp.ClientSession(base_url=url, headers=headers)
    logger.debug(f"Created session with base url {url}")
    return session


async def _list_pages(session: aiohttp.ClientSession) -> List[PageListItem]:
    """
    List all pages in wiki

    Args:
        session: aiohttp session

    Returns:
        List of pages
    """

    query = """
    query {
        pages {
            list (orderBy: TITLE) {
                id
                path
                title
            }
        }
    }
    """
    logger.debug("Listing pages from wiki on url: %s", session._base_url)
    resp = await session.post("/graphql", json={"query": query})

    logger.debug(
        "Got response from wiki. Response status: %s, Response text: %s",
        resp.status,
        await resp.text(),
    )
    data = await resp.json()

    logger.debug("Json: %s", data)
    pages_ = data["data"]["pages"]["list"]
    pages = [PageListItem(**item) for item in pages_]
    return pages


async def _get_page(
    session: aiohttp.ClientSession, page_id: int, locale: str
) -> Page | None:
    """Get page with content

    Args:
        session: aiohttp session
        page_id: Page ID

    Returns:
        Page or None if page does not exist or is not accessible (unauthorized)
    """
    query = """
    query ($id: Int!) {
        pages {
            single(id: $id) {
                id
                path
                title
                description
                content
            }
        }
    }
    """
    logger.debug("Getting page with id %s", page_id)
    resp = await session.post(
        "/graphql", json={"query": query, "variables": {"id": page_id}}
    )
    logger.debug(
        "Got response from wiki for Page with id %s. Response status: %s, Response text: %s",
        page_id,
        resp.status,
        await resp.text(),
    )

    data = await resp.json()
    if session._base_url is None:
        raise ValueError("Base url is None")
    try:
        page = Page(
            **data["data"]["pages"]["single"],
            instance_url=str(session._base_url),
            locale=locale,
        )
    except TypeError:
        return None
    return page


def save_documents_to_xlsx(documents: List[Document], outfile: Path):
    """Save documents to xlsx file

    Args:
        documents: List of documents
        outfile: Path to output file
    """
    from openpyxl import Workbook
    from openpyxl.worksheet.worksheet import Worksheet

    # Create workbook
    wb = Workbook()
    # Open first sheet
    ws: Worksheet | None = wb.active  # type: ignore
    if ws is None:
        raise ValueError("No worksheet")

    # Add header
    ws.append(["Text", "Source"])

    for document in documents:
        ws.append(
            [
                document.page_content,
                document.metadata["source"],
            ]
        )

    wb.save(outfile)


class WikiJSLoader(BaseLoader):
    """Load all pages from WikiJS instance.add()

    Args:
        url: Url of WikiJS instance
        token: Authentication token
        locale: Locale of pages to load. For example "pl" or "en"
        text_splitter: Text splitter to use to split pages into smaller chunks
        add_path_to_contents: Whether to add source path to content of Document. Example: '{text}\nŹródło: path/to/page'
        add_desc_to_contents: Whether to add description to content of Document. Example: 'Opis strony: {text}\'
    """

    def __init__(
        self,
        url: str,
        token: str,
        locale: str,
        text_splitter: Optional[TextSplitter] = None,
        add_path_to_contents: bool = False,
        add_desc_to_contents: bool = False,
    ) -> None:
        self.url = url
        self.token = token
        self.locale = locale
        self.text_splitter = text_splitter
        self.add_path_to_contents = add_path_to_contents
        self.add_desc_to_contents = add_desc_to_contents

        # Create session and event loop for async operations
        self.loop = asyncio.get_event_loop()
        self.session = _get_session(self.url, self.token)

    def load(self) -> List[Document]:
        page_items = self.loop.run_until_complete(_list_pages(self.session))
        pages = self.loop.run_until_complete(
            asyncio.gather(
                *[_get_page(self.session, page.id, self.locale) for page in page_items]
            )
        )

        # Filter out None values
        pages = [page for page in pages if page is not None]

        # Apply splitter
        documents = []
        if self.text_splitter is not None:
            for page in pages:
                texts = self.text_splitter.split_text(page.content)

                documents.extend(
                    self.text_splitter.create_documents(
                        texts, [page.metadata] * len(texts)
                    )
                )
        else:
            documents = [page.to_document() for page in pages]

        for document in documents:
            if self.add_path_to_contents:
                document.page_content += f"\nŹródło: {document.metadata['path']}"
            if self.add_desc_to_contents:
                document.page_content = (
                    f"Opis strony: {document.metadata['description']}\n"
                    + document.page_content
                )

        return documents

    def __del__(self) -> None:
        self.loop.run_until_complete(self.session.close())
        if not self.loop.is_running():  # TODO: Check if this is needed
            # Close loop if it is not running (e.g. if it was created by this class)
            # This is needed to prevent "Unclosed event loop" warning
            self.loop.close()


def cli():
    import argparse
    from pprint import pprint
    from dotenv import load_dotenv
    import os
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    load_dotenv()

    parser = argparse.ArgumentParser(
        description="""WikiJS Downloader. Downloads all pages from WikiJS instance and stores them in a xslx file.

Requires WIKIJS_TOKEN environment variable to be set. The environment variables are automatically loaded from .env file in current directory.

Example usage (after installing with pip):
    wikijs-save-documents http://localhost:3000 -o documents.xlsx
"""
    )
    parser.add_argument("url", metavar="URL", type=str)
    parser.add_argument("-s", "--split", action="store_true")
    parser.add_argument(
        "-o", "--out-file", metavar="OUTFILE", type=Path, default="documents.xslx"
    )
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument(
        "--add-path",
        action="store_true",
        help="Add source path to content of Document. Example: '{text}\nŹródło: path/to/page'",
    )
    parser.add_argument(
        "--add-desc",
        action="store_true",
        help="Add description to content of Document. Example: 'Opis strony: {text}'",
    )

    if parser.parse_args().debug:
        # create console handler and set level to debug
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)
    args = parser.parse_args()

    url = args.url
    token = os.getenv("WIKIJS_TOKEN")
    if token is None:
        raise ValueError("WIKIJS_TOKEN is not defined in environment variables")

    text_splitter = None
    if args.split is not None:
        text_splitter = RecursiveCharacterTextSplitter(
            # Set a really small chunk size, just to show.
            chunk_size=700,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )

    loader = WikiJSLoader(
        url,
        token,
        "pl",
        text_splitter=text_splitter,
        add_path_to_contents=args.add_path,
        add_desc_to_contents=args.add_desc,
    )
    documents = loader.load()

    if args.out_file:
        save_documents_to_xlsx(documents, args.out_file)
    else:
        pprint(documents)

    # # Embed and store splits

    # from langchain.vectorstores import Chroma
    # from langchain.embeddings import OpenAIEmbeddings

    # vectorstore = Chroma.from_documents(
    #     documents=documents, embedding=OpenAIEmbeddings()
    # )
    # retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # # Prompt
    # # https://smith.langchain.com/hub/rlm/rag-prompt

    # from langchain import hub

    # rag_prompt = hub.pull("rlm/rag-prompt")

    # # LLM

    # from langchain.chat_models import ChatOpenAI

    # llm = ChatOpenAI(temperature=0, max_tokens=500)

    # # RAG chain

    # from langchain.schema.runnable import RunnablePassthrough

    # rag_chain = (
    #     {"context": retriever, "question": RunnablePassthrough()} | rag_prompt | llm
    # )

    # pprint(rag_chain.invoke("Jakie zasoby lub serwery ma koło?"))
