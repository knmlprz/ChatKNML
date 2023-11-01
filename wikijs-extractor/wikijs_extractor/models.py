from pydantic import BaseModel, ConfigDict, HttpUrl, computed_field
from urllib.parse import urljoin

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
    def url(self) -> HttpUrl:
        # Url pf page is instance url / locale / path
        return HttpUrl(urljoin(self.instance_url, f"{self.locale}/{self.path}"))
