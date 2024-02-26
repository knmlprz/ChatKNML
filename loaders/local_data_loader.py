from langchain.document_loaders.base import BaseLoader
from langchain.document_loaders import PyPDFLoader, JSONLoader
from langchain.document_loaders.text import TextLoader
from langchain.document_loaders.csv_loader import CSVLoader
from typing import Union, List
import os


class LocalDataLoader(BaseLoader):

    loaders = {
        ".pdf": PyPDFLoader,
        ".json": JSONLoader,
        ".txt": TextLoader,
        ".csv": CSVLoader,
    }

    def __init__(self, path: Union[List[str], str]):
        """
        Initialize the LocalDataLoader instance.

        :param path: A list of paths or a single path pointing to the location of data files.
        """
        super().__init__()
        self.path_list = path

    @staticmethod
    def ds_converter(docs):
        """
        Converts a list of documents into a specific data structure.

        :param docs: List of documents to be converted.
        :return: List of dictionaries, each representing a document with 'text' and 'url' keys.
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
            if doc.page_content not in seen_texts and doc not in junk_docs:
                clear_docs.append(doc)
                seen_texts.add(doc.page_content)
            else:
                pass
        return clear_docs

    def load(self) -> List[dict]:
        """
        Load data from the specified paths using registered data loaders.

        This method iterates through each path in the 'path_list', explores the directories, and processes each file
        using the appropriate data loader based on the file extension. The loaded data is then appended to a list,
        which is further processed to remove junk and convert the data structure. The final list of dictionaries is returned.

        :return: A list of dictionaries representing the loaded and processed data.
        """
        docs = []
        for path in self.path_list:
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    d_type = os.path.splitext(file_path)[1].lower()
                    if d_type in LocalDataLoader.loaders:
                        loader = LocalDataLoader.loaders[d_type](file_path)
                        try:
                            docs.append(loader.load()[0])
                        except Exception as e:
                            print(f"Exception: {e}")
                            continue

        docs = LocalDataLoader.junk_remover(docs)
        docs = LocalDataLoader.ds_converter(docs)
        return docs
