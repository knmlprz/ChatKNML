from typing import List

import pytest
from langchain.docstore.document import Document


@pytest.fixture
def documents_with_source() -> List[Document]:
    return [
        Document(page_content="content1", metadata={"source": "source1"}),
        Document(page_content="content2", metadata={"source": "source2"}),
        Document(page_content="content3", metadata={"source": "source3"}),
    ]
