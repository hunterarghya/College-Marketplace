from pydantic import BaseModel
from typing import Optional, List

class Post_item(BaseModel):
    title: str
    description: str
    price: int
    location: str

    