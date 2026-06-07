from typing import List
from fastapi import APIRouter, HTTPException
from starlette import status
from taskflow.app.users.user_schema import UserDisplay, UserCreate, UserUpdate
from taskflow.app.users.validators import validate_email_availability
from taskflow.app.users.user_repository import (
    get_users,
    get_user_by_id,
    create_user_db,
    update_user,
    delete_user
)
from taskflow.app.users.user_service import get_user_by_id as get_user_id
from taskflow.app.users.user_service import create_user, hash_password


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", status_code=status.HTTP_200_OK)
def list_users():
    return get_users()

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int):
    return get_user_id(user_id)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    return create_user_db(
        username=user.username,
        email=user.email,
        password_hash = hash_password(user.password)
    )

@router.put("/{user_id}", status_code=status.HTTP_200_OK)
def edit_user(user_id: int, username: str, email: str):
    
    existing_user = get_user_by_id(user_id)
    
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return update_user(user_id, username, email)

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def remove_user(user_id: int):
    
    existing_user = get_user_by_id(user_id)
    
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    delete_user(user_id)
    return {"message": "user deleted successfully"}