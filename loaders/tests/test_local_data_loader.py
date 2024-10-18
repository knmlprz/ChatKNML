import pytest
from loaders.local_data_loader import LocalDataLoader
from langchain_core.documents import Document


@pytest.fixture
def local_data_loader():
    path = "/path/to/data/files"
    return LocalDataLoader(path)


def test_ds_converter():
    docs = [Document(page_content="Document 1"), Document(page_content="Document 2")]
    expected_output = [{"text": "Document 1"}, {"text": "Document 2"}]
    assert LocalDataLoader.ds_converter(docs) == expected_output


def test_junk_remover(local_data_loader):
    doc_1 = Document(
        page_content="Curabitur mattis luctus arcu vestibulum tristique. Proin ac suscipit arcu. Mauris massa nisl, condimentum eget vestibulum eu, facilisis ut quam. Curabitur vitae magna et ante auctor condimentum. Phasellus placerat dictum est eu tincidunt. Curabitur nec porttitor velit.Phasellus placerat dictum est eu tincidunt. Curabitur nec porttitor velit. Curabitur nec porttitor velit. Curabitur nec porttitor velit."
    )
    doc_2 = Document(page_content="")
    doc_3 = Document(
        page_content="Curabitur mattis luctus arcu vestibulum tristique. Proin ac suscipit arcu. Mauris massa nisl, condimentum eget vestibulum eu, facilisis ut quam. Curabitur vitae magna et ante auctor condimentum. Phasellus placerat dictum est eu tincidunt. Curabitur nec porttitor velit.Phasellus placerat dictum est eu tincidunt. Curabitur nec porttitor velit. Curabitur nec porttitor velit. Curabitur nec porttitor velit."
    )
    doc_4 = Document(page_content="Short document.")
    doc_5 = Document(
        page_content="A proper document, over 300 words long, occurring only once. A proper document, over 300 words long, occurring only once. A proper document, over 300 words long, occurring only once. A proper document, over 300 words long, occurring only once. A proper document, over 300 words long, occurring only once. A proper document, over 300 words long, occurring only once."
    )
    docs = [doc_1, doc_2, doc_3, doc_4, doc_5]

    expected_output = [doc_1, doc_5]

    result = local_data_loader.junk_remover(docs)
    assert result == expected_output
