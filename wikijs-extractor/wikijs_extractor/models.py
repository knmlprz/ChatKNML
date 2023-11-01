from pydantic import BaseModel, ConfigDict, HttpUrl, computed_field
from urllib.parse import urljoin

from langchain.docstore.document import Document

class PageListItem(BaseModel):
    # Allow extra fields
    model_config = ConfigDict(extra="allow")

    id: int
    path: str
    title: str


class Page(BaseModel):
    # Allow extra fields
    model_config = ConfigDict(extra="allow")

    id: int
    path: str
    title: str
    description: str
    content: str
    locale: str
    instance_url: str
    
    @computed_field
    @property
    def source(self) -> HttpUrl:
        # Url pf page is instance url / locale / path
        return HttpUrl(urljoin(self.instance_url, f"{self.locale}/{self.path}"))
    
    def to_document(self) -> Document:
        return Document(
            page_content=self.content,
            metadata={
                "id": self.id,
                "path": self.path,
                "title": self.title,
                "description": self.description,
                "locale": self.locale,
                "instance_url": self.instance_url,
                "source": self.source,
            }
        )
