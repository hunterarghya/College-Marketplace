from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Custom fields
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    upi_id = Column(String, nullable=False)

    posts = relationship("PostItems", back_populates="user")


class PostItems(Base):
    __tablename__ = "post_items"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)
    location = Column(String)
    url= Column(String)
    file_type= Column(String)
    file_name= Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    status= Column(String, nullable=False, default="available")

    user = relationship("User", back_populates="posts")
