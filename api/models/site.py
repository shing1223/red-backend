from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class WebsiteSubmit(BaseModel):
    url: HttpUrl
    title: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = None
    region: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = []
    

class WebsiteResult(BaseModel):
    id: int
    url: HttpUrl
    title: Optional[str]
    description: Optional[str]
    language: Optional[str]
    region: Optional[str]
    category: Optional[str]
    tags: List[str]
    favicon: Optional[str]
    og_image: Optional[str]
    score: float