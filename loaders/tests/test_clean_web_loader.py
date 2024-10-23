import pytest
from loaders.clean_web_loader import CleanWebLoader
from langchain_core.documents import Document


@pytest.fixture
def clean_web_loader():
    url_list = ["https://example.com"]
    return CleanWebLoader(url_list)


def test_newspaper_extractor():
    html = "<html><body><p>This is some text.</p></body></html>"
    expected_output = "This is some text."
    assert CleanWebLoader.newspaper_extractor(html) == expected_output


def test_ds_converter(clean_web_loader):
    docs = [Document(page_content="Document 1"), Document(page_content="Document 2")]
    expected_output = [{"text": "Document 1"}, {"text": "Document 2"}]
    assert clean_web_loader.ds_converter(docs) == expected_output


def test_junk_remover(clean_web_loader):
    doc_1 = Document(
        page_content="Curabitur mattis luctus arcu vestibulum tristique. Proin ac suscipit arcu. Mauris massa nisl, condimentum eget vestibulum eu, facilisis ut quam. Curabitur vitae magna et ante auctor condimentum. Phasellus placerat dictum est eu tincidunt. Curabitur nec porttitor velit.Phasellus placerat dictum est eu tincidunt. Curabitur nec porttitor velit. Curabitur nec porttitor velit. Curabitur nec porttitor velit.",
        metadata={"title": None, "key2": None, "key3": None},
    )
    doc_2 = Document(page_content="", metadata={"key2": None, "key3": None})
    doc_3 = Document(
        page_content="Curabitur mattis luctus arcu vestibulum tristique. Proin ac suscipit arcu. Mauris massa nisl, condimentum eget vestibulum eu, facilisis ut quam. Curabitur vitae magna et ante auctor condimentum. Phasellus placerat dictum est eu tincidunt. Curabitur nec porttitor velit.Phasellus placerat dictum est eu tincidunt. Curabitur nec porttitor velit. Curabitur nec porttitor velit. Curabitur nec porttitor velit.",
        metadata={"title": None, "key3": None},
    )
    doc_4 = doc_1
    doc_5 = Document(
        page_content="Short document.",
        metadata={"title": None, "key2": None, "key3": None},
    )
    doc_6 = Document(
        page_content="A proper document, over 300 words long, occurring only once. A proper document, over 300 words long, occurring only once. A proper document, over 300 words long, occurring only once. A proper document, over 300 words long, occurring only once. A proper document, over 300 words long, occurring only once. A proper document, over 300 words long, occurring only once.",
        metadata={"title": None, "key2": None, "key3": None},
    )
    docs = [doc_1, doc_2, doc_3, doc_4, doc_5, doc_6]

    expected_output = [doc_1, doc_6]

    result = clean_web_loader.junk_remover(docs)
    assert result == expected_output
