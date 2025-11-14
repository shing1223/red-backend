from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional

class WebsiteSubmit(BaseModel):
    url: HttpUrl
    title: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = None
    region: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class WebsiteResult(BaseModel):
    id: int
    url: HttpUrl
    title: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = None
    region: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    favicon: Optional[str] = None
    og_image: Optional[str] = None
    score: float