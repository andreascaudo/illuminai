from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.user import User, UserCreate, UserUpdate
from utils.auth import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str):
    """
    Get a user by email
    """
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str):
    """
    Get a user by username
    """
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    """
    Get a user by ID
    """
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    """
    Create a new user
    """
    # Check if email already exists
    db_user_email = get_user_by_email(db, user.email)
    if db_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    db_user_username = get_user_by_username(db, user.username)
    if db_user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    """
    Update an existing user
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_data = user_update.dict(exclude_unset=True)
    
    # Check if email is being updated and if it already exists
    if user_data.get("email") and user_data["email"] != db_user.email:
        existing_user = get_user_by_email(db, user_data["email"])
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Check if username is being updated and if it already exists
    if user_data.get("username") and user_data["username"] != db_user.username:
        existing_user = get_user_by_username(db, user_data["username"])
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Handle password update
    if user_data.get("password"):
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
    
    # Update user
    for key, value in user_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    
    return db_user

def verify_user_password(db: Session, user_id: int, password: str):
    """
    Verify a user's password
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    
    return verify_password(password, db_user.hashed_password)