from langchain.document_loaders.base import BaseLoader
from langchain.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain.text_splitter import TextSplitter, SpacyTextSplitter
from newspaper import Article
from typing import Union, List, Optional
from functools import reduce


class CleanWebLoader(BaseLoader):
    """
    A class for loading web content, extracting and cleaning text using the 'newspaper' library,
    and converting it into a specific data structure.

    Attributes:
        url_list (Union[List[str], str]): Either a string or a list of strings representing URLs.
        depth (int): Maximum depth for recursive extraction (default is 1).

    Methods:
        newspaper_extractor(html): Extracts and cleans text content from HTML using the 'newspaper' library.
        ds_converter(docs): Converts a list of documents into a specific data structure.
        junk_remover(docs): Identifies and returns a list of suspected junk documents based on specific criteria.
        load(): Loads web content from specified URLs, extracts text, and converts it into a specific data structure.
        load_and_split(text_splitter, chunk, chunk_overlap): Loads web content, splits it into chunks, and converts it into a specific data structure.

    """

    article = Article("")

    def __init__(self, url_list: Union[List[str], str], depth: int = 1):
        """
        Initializes the CleanWebLoader instance.

        :param url_list: Either a string or a list of strings representing URLs.
        :param depth: Maximum depth for recursive extraction (default is 1).
        """
        super().__init__()
        self.url_list = url_list
        self.depth = depth

    @staticmethod
    def newspaper_extractor(html):
        """
        Extracts and cleans text content from HTML using the 'newspaper' library.

        :param html: HTML content to be processed.
        :return: Cleaned and concatenated text extracted from the HTML.
        """
        CleanWebLoader.article.set_html(html)
        CleanWebLoader.article.parse()
        return " ".join(CleanWebLoader.article.text.split())

    @staticmethod
    def ds_converter(docs):
        """
        Converts a list of documents into a specific data structure.

        :param docs: List of documents to be converted.
        :return: List of dictionaries, each representing a document with 'text' key.
        """
        return [{"text": doc.page_content} for doc in docs]

    @staticmethod
    def junk_remover(docs):
        """
        Identifies and returns a list of suspected junk documents based on specific criteria.

        :param docs: A list of documents, where each document is represented as a dictionary.
                    Each dictionary should have a "text" key containing the text content of the document.
        :return: A list of suspected junk documents based on the criteria of having less than 300 characters
                or having the same text as another document in the input list.
        """
        junk_docs = [doc for doc in docs if len(doc.page_content) < 300]
        seen_texts = set()
        clear_docs = []
        for doc in docs:
            if "title" not in doc.metadata.keys():
                junk_docs.append(doc)
            elif doc.page_content not in seen_texts and doc not in junk_docs:
                clear_docs.append(doc)
                seen_texts.add(doc.page_content)
            else:
                pass
        return clear_docs

    def load(self) -> List[dict]:
        """
        Loads web content from specified URLs, extracts text using the 'newspaper' library,
        and converts it into a specific data structure using the ds_converter and junk_remover methods.

        :return: List of dictionaries, each representing a document with 'text' key.
        """
        docs = []
        if isinstance(self.url_list, str):
            self.url_list = [self.url_list]
        for address in self.url_list:
            try:
                loader = RecursiveUrlLoader(
                    url=address,
                    max_depth=self.depth,
                    extractor=CleanWebLoader.newspaper_extractor,
                )
                docs.extend(loader.load())
            except Exception as e:
                print(f"Exception: {e}")
                break
        docs = reduce(
            lambda data, method: method(data),
            [CleanWebLoader.junk_remover, CleanWebLoader.ds_converter],
            docs,
        )
        return docs

    def load_and_split(
        self,
        text_splitter: Optional[TextSplitter] = None,
        chunk: int = 400,
        chunk_overlap: int = 80,
    ) -> List[dict]:
        """
        Loads web content from specified URLs, extracts text using the 'newspaper' library,
        splits it into chunks using the provided or default TextSplitter,
        and converts it into a specific data structure using the ds_converter and junk_remover methods.

        :param text_splitter: Optional TextSplitter instance to use for splitting documents.
        :param chunk: Chunk size for text splitting (default is 400).
        :param chunk_overlap: Overlap size between chunks (default is 80).
        :return: List of dictionaries, each representing a document with 'text' key.
        """
        if text_splitter is None:
            _text_splitter: TextSplitter = SpacyTextSplitter(
                pipeline="pl_core_news_sm",
                chunk_size=chunk,
                chunk_overlap=chunk_overlap,
            )
        else:
            _text_splitter = text_splitter
        docs = self.load()
        docs = reduce(
            lambda data, method: method(data),
            [CleanWebLoader.junk_remover, CleanWebLoader.ds_converter],
            docs,
        )
        return _text_splitter.split_documents(docs)
