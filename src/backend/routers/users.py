from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from models.user import User, UserResponse, UserUpdate
from utils.auth import get_current_user, get_password_hash

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get information about the currently authenticated user
    """
    return current_user

@router.put("/me", response_model=UserResponse)
def update_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update the currently authenticated user's information
    """
    user_data = user_update.dict(exclude_unset=True)
    
    # If email is being updated, check if it already exists
    if user_data.get("email") and user_data["email"] != current_user.email:
        db_user = db.query(User).filter(User.email == user_data["email"]).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # If username is being updated, check if it already exists
    if user_data.get("username") and user_data["username"] != current_user.username:
        db_user = db.query(User).filter(User.username == user_data["username"]).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # If password is being updated, hash it
    if user_data.get("password"):
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
    
    # Update user
    for key, value in user_data.items():
        setattr(current_user, key, value)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user