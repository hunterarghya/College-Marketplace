from sqlalchemy import Column, String, Text, JSON, Integer, DateTime
from app.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class PostItems(Base):
    __tablename__ = "post_items"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable= False)
    location = Column(String)
    url= Column(String)
    file_type= Column(String)
    file_name= Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    status= Column(String, nullable=False, default="available")
