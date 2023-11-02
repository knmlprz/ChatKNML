import pytest  # noqa: F401

# Required for fixtures to work
from .fixtures import documents_with_source  # noqa: F401

from typing import List
from langchain.docstore.document import Document
from pathlib import Path

from tempfile import TemporaryDirectory

from wikijs_extractor.loaders import save_documents_to_xlsx, load_xslx_to_documents


def test_xslx(documents_with_source: List[Document]):  # noqa: F811
    # Create temporary directory
    temp_dir = TemporaryDirectory()
    # Create temporary file
    temp_file = Path(temp_dir.name) / "test.xlsx"
    # Save documents to xlsx
    save_documents_to_xlsx(documents=documents_with_source, outfile=temp_file)
    # Load documents from xlsx
    documents = load_xslx_to_documents(infile=temp_file)
    # Check that documents are equal
    assert documents == documents_with_source
    # Close temporary directory
    temp_dir.cleanup()
