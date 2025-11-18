from pydantic import BaseModel
from typing import Optional, List

class Post_item(BaseModel):
    title: str
    description: str
    price: int
    location: str

class PostUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    location: Optional[str] = None