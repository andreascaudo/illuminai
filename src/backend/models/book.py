from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime
from pydantic import BaseModel
import enum

class BookFormat(str, enum.Enum):
    EPUB = "epub"
    PDF = "pdf"
    TXT = "txt"

class Book(Base):
    """SQLAlchemy Model for books table"""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True)
    cover_image_url = Column(String, nullable=True)
    file_path = Column(String, nullable=False)
    format = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)  # Size in bytes
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
    # Relationship with User model
    owner = relationship("User", back_populates="books")

# Add this to User model to establish relationship
# books = relationship("Book", back_populates="owner")

# Pydantic models for API validation

class BookBase(BaseModel):
    title: str
    author: str = None
    description: str = None

class BookCreate(BookBase):
    format: BookFormat

class BookResponse(BookBase):
    id: int
    cover_image_url: str = None
    format: str
    file_size: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class BookUpdate(BaseModel):
    title: str = None
    author: str = None
    description: str = None