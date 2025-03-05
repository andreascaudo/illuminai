from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
import uuid
from database.database import get_db
from models.book import Book, BookResponse, BookCreate, BookUpdate, BookFormat
from models.user import User
from utils.auth import get_current_user
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Ensure upload directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class BookUploadResponse(BaseModel):
    message: str
    book: BookResponse


@router.get("/", response_model=List[BookResponse])
def get_user_books(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print("Endpoint /api/books was called")  # Check if the endpoint is hit
    print(f"Current user: {current_user.username}")
    logger.error(f"Current user: {current_user.username}")
    # Log the current user
    logger.info(f"Current user: {current_user.username}")
    """
    Get all books belonging to the current user
    """
    logger.info(f"Getting books for user: {current_user.id}")
    books = db.query(Book).filter(
        Book.user_id == current_user.id).offset(skip).limit(limit).all()
    # debug book
    logger.info(f"Books retrieved: {books}")
    return books


@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific book by ID
    """
    book = db.query(Book).filter(Book.id == book_id,
                                 Book.user_id == current_user.id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book


@router.post("/upload", response_model=BookUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_book(
    file: UploadFile = File(...),
    title: str = Form(...),
    author: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a new book file
    """
    # Validate file format
    file_ext = os.path.splitext(file.filename)[1].lower().replace(".", "")
    if file_ext not in [e.value for e in BookFormat]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format. Supported formats: {', '.join([e.value for e in BookFormat])}"
        )

    # Create user-specific upload directory
    user_upload_dir = os.path.join(UPLOAD_DIR, str(current_user.id))
    os.makedirs(user_upload_dir, exist_ok=True)

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(user_upload_dir, unique_filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Get file size
    file_size = os.path.getsize(file_path)

    # Create book record in database
    db_book = Book(
        title=title,
        author=author,
        description=description,
        file_path=file_path,
        format=file_ext,
        file_size=file_size,
        user_id=current_user.id
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return {"message": "Book uploaded successfully", "book": db_book}


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book_update: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update book metadata
    """
    book = db.query(Book).filter(Book.id == book_id,
                                 Book.user_id == current_user.id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    book_data = book_update.dict(exclude_unset=True)
    for key, value in book_data.items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)

    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a book
    """
    book = db.query(Book).filter(Book.id == book_id,
                                 Book.user_id == current_user.id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    # Delete the file
    if os.path.exists(book.file_path):
        os.remove(book.file_path)

    # Delete the record
    db.delete(book)
    db.commit()

    return None
