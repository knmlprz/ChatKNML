import aiohttp
import asyncio
import logging

from typing import List

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader

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


class WikiJSLoader(BaseLoader):
    """Load all pages from WikiJS instance"""

    url: str
    token: str
    locale: str

    def __init__(self, url: str, token: str, locale: str) -> None:
        self.url = url
        self.token = token
        self.locale = locale

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
        documents = [page.to_document() for page in pages if page is not None]
        return documents

    def __del__(self) -> None:
        self.loop.run_until_complete(self.session.close())
        if not self.loop.is_running():
            # Close loop if it is not running (e.g. if it was created by this class)
            # This is needed to prevent "Unclosed event loop" warning
            self.loop.close()


def cli():
    import argparse
    from pprint import pprint
    from dotenv import load_dotenv
    import os

    load_dotenv()

    parser = argparse.ArgumentParser(description="WikiJS Downloader")
    parser.add_argument("url", metavar="URL", type=str)
    parser.add_argument("-o", "--output", metavar="OUTPUT", type=str, default="output")
    parser.add_argument("-d", "--debug", action="store_true")

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

    loader = WikiJSLoader(url, token, "pl")
    documents = loader.load()

    pprint(documents)
