from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
from datetime import datetime

# Post schemas
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

# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    phone: str
    upi_id: str

class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool
    name: str
    phone: str
    upi_id: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
