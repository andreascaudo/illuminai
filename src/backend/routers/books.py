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


from fastapi.responses import FileResponse, StreamingResponse
import io

@router.get("/{book_id}/content")
async def get_book_content(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get the content of a book file
    """
    book = db.query(Book).filter(Book.id == book_id,
                               Book.user_id == current_user.id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    if not os.path.exists(book.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book file not found"
        )
    
    # Different responses based on file format
    if book.format == "txt":
        # For text files, read the content and return it
        try:
            with open(book.file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return {"content": content}
        except UnicodeDecodeError:
            # Try with a different encoding if UTF-8 fails
            with open(book.file_path, "r", encoding="latin-1") as f:
                content = f.read()
            return {"content": content}
    elif book.format == "epub":
        # For EPUB files, add cache control headers to prevent caching
        headers = {
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
        return FileResponse(
            book.file_path,
            filename=f"{book.title}.{book.format}",
            media_type=get_media_type(book.format),
            headers=headers
        )
    else:
        # For other binary files (e.g., pdf), serve the file directly
        return FileResponse(
            book.file_path,
            filename=f"{book.title}.{book.format}",
            media_type=get_media_type(book.format)
        )

def get_media_type(format: str) -> str:
    """
    Get the appropriate media type for a given file format
    """
    media_types = {
        "epub": "application/epub+zip",
        "pdf": "application/pdf",
        "txt": "text/plain"
    }
    return media_types.get(format, "application/octet-stream")


import zipfile
from fastapi.responses import Response
from pathlib import Path

# Explicitly allow open access to EPUB internal files
@router.get("/{book_id}/{file_path:path}", dependencies=[])
async def get_epub_file(
    book_id: int,
    file_path: str,
    db: Session = Depends(get_db),
):
    """
    Serve internal files from EPUB archive
    """
    # Get the book without user verification for EPUB internal files
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    if not os.path.exists(book.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book file not found"
        )
    
    # Only serve internal files from EPUB
    if book.format != "epub":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only EPUB format supports accessing internal files"
        )
    
    try:
        with zipfile.ZipFile(book.file_path, 'r') as epub_file:
            # Check if the requested file exists in the EPUB
            try:
                file_info = epub_file.getinfo(file_path)
                file_content = epub_file.read(file_path)
            except KeyError:
                # Log the error for debugging
                logger.error(f"File {file_path} not found in EPUB book {book_id}")
                logger.error(f"Available files: {epub_file.namelist()}")
                
                # Try to find a case-insensitive match
                lowercased_path = file_path.lower()
                for name in epub_file.namelist():
                    if name.lower() == lowercased_path:
                        file_content = epub_file.read(name)
                        file_path = name  # Use the correct case for content type determination
                        break
                else:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"File {file_path} not found in EPUB"
                    )
            
            # Determine content type based on file extension
            extension = Path(file_path).suffix.lower().lstrip('.')
            content_type = {
                'html': 'text/html',
                'xhtml': 'application/xhtml+xml',
                'htm': 'text/html',
                'css': 'text/css',
                'js': 'application/javascript',
                'xml': 'application/xml',
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'png': 'image/png',
                'gif': 'image/gif',
                'svg': 'image/svg+xml',
                'ttf': 'font/ttf',
                'otf': 'font/otf',
                'woff': 'font/woff',
                'woff2': 'font/woff2',
                'ncx': 'application/x-dtbncx+xml',
                'opf': 'application/oebps-package+xml',
            }.get(extension, 'application/octet-stream')
            
            # Set cache control headers
            headers = {
                "Cache-Control": "public, max-age=3600",
                "Access-Control-Allow-Origin": "*"
            }
            
            return Response(
                content=file_content, 
                media_type=content_type,
                headers=headers
            )
    except zipfile.BadZipFile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid EPUB file"
        )
