import os
import logging
from langchain.document_loaders.base import BaseLoader
from langchain.document_loaders import PyPDFLoader, JSONLoader
from langchain.document_loaders.text import TextLoader
from langchain.document_loaders.csv_loader import CSVLoader
from typing import Union, List


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
        seen_texts = {}
        clear_docs = []
        for doc in docs:
            if doc.page_content not in seen_texts and doc not in junk_docs:
                clear_docs.append(doc)
                seen_texts.add(doc.page_content)
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
            docs.extend(self._process_directory(path))

        docs = self._process_loaded_data(docs)
        return docs

    def _process_directory(self, path: str) -> List[dict]:
        """
        Process all files in the given directory path using the appropriate loaders.

        :param path: The path to the directory containing the files.
        :return: A list of dictionaries with loaded data.
        """
        loaded_docs = []
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                doc = self._load_file(file_path)
                if doc:
                    loaded_docs.append(doc)
        return loaded_docs

    def _load_file(self, file_path: str) -> dict:
        """
        Load a single file using the appropriate loader based on its extension.

        :param file_path: The full path to the file.
        :return: A dictionary with loaded data or None if an error occurred.
        """
        file_extension = os.path.splitext(file_path)[1].lower()
        loader = LocalDataLoader.loaders.get(file_extension)
        
        if loader:
            try:
                return loader(file_path).load()[0]
            except Exception as e:
                logging.error(f"Error loading file {file_path}: {e}")
        else:
            logging.warning(f"No loader found for file type: {file_extension}")
        return None

    def _process_loaded_data(self, docs: List[dict]) -> List[dict]:
        """
        Process loaded data by removing junk and converting the data structure.

        :param docs: A list of dictionaries with raw loaded data.
        :return: A list of dictionaries with cleaned and processed data.
        """
        docs = LocalDataLoader.junk_remover(docs)
        return LocalDataLoader.ds_converter(docs)
