from typing import List
from fastapi import APIRouter
from taskflow.app.users.user_schema import UserDisplay, UserCreate, UserUpdate
from taskflow.app.core.security import hash_password
from taskflow.app.users.user_repository import (
    get_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/")
def list_users():
    return get_users()

@router.get("/{user_id}")
def get_user(user_id: int):
    return get_user_by_id(user_id)

@router.post("/")
def add_user(user: UserCreate):
    hashed_password = hash_password(user.password)
    return create_user(
        username=user.username,
        email=user.email,
        password_hash = hashed_password
    )

@router.put("/{user_id}")
def edit_user(user_id: int, username: str, email: str):
    return update_user(user_id, username, email)

@router.delete("/{user_id}")
def remove_user(user_id: int):
    return delete_user(user_id)