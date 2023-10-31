from pydantic import BaseModel, ConfigDict


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
