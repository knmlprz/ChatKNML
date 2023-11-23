"""Pydantic models for WikiJS's Grapghql API."""

from urllib.parse import urljoin

from langchain.docstore.document import Document
from pydantic import BaseModel, ConfigDict, computed_field


class PageListItem(BaseModel):
    """PageListItem from WikiJS's Graphql API."""

    # Allow extra fields
    model_config = ConfigDict(extra="allow")

    path: str
    title: str

    def __hash__(self) -> int:
        """Required for this object to be hashable."""
        return hash(self.path)


class Page(BaseModel):
    """Page from WikiJS's Graphql API."""

    # Allow extra fields
    model_config = ConfigDict(extra="allow")

    path: str
    title: str
    description: str
    content: str
    locale: str
    instance_url: str

    @computed_field
    @property
    def source(self) -> str:
        """Source of page (url/locale/path)."""
        # Url page is: instance url / locale / path
        return urljoin(self.instance_url, f"{self.locale}/{self.path}")

    @property
    def metadata(self) -> dict[str, str | int | float | bool]:
        """Convert page to metadata."""
        return {
            "id": self.id,
            "path": self.path,
            "title": self.title,
            "description": self.description,
            "locale": self.locale,
            "instance_url": self.instance_url,
            "source": self.source,
        }

    def to_document(self) -> Document:
        """Convert page to Langchain's `Document`."""
        return Document(
            page_content=self.content,
            metadata=self.metadata,
        )
