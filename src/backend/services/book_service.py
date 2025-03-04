from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
import os
import shutil
import uuid
from models.book import Book, BookCreate

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def create_book(
    file: UploadFile,
    title: str,
    author: str | None,
    description: str | None,
    user_id: int,
    db: Session
) -> Book:
    """
    Create a new book from an uploaded file
    """
    # Validate file format
    file_ext = os.path.splitext(file.filename)[1].lower().replace(".", "")
    valid_formats = ["epub", "pdf", "txt"]
    
    if file_ext not in valid_formats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format. Supported formats: {', '.join(valid_formats)}"
        )
    
    # Create user-specific upload directory
    user_upload_dir = os.path.join(UPLOAD_DIR, str(user_id))
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
        user_id=user_id
    )
    
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    
    return db_book

def get_user_books(user_id: int, skip: int, limit: int, db: Session):
    """
    Get all books for a specific user
    """
    return db.query(Book).filter(Book.user_id == user_id).offset(skip).limit(limit).all()

def get_book_by_id(book_id: int, user_id: int, db: Session):
    """
    Get a specific book by ID, ensuring it belongs to the current user
    """
    book = db.query(Book).filter(Book.id == book_id, Book.user_id == user_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book

def delete_book(book_id: int, user_id: int, db: Session):
    """
    Delete a book and its file
    """
    book = get_book_by_id(book_id, user_id, db)
    
    # Delete the file
    if os.path.exists(book.file_path):
        os.remove(book.file_path)
    
    # Delete the record
    db.delete(book)
    db.commit()
    
    return True