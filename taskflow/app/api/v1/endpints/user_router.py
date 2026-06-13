from typing import List
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from taskflow.app.api.dependencies import get_db
from taskflow.app.schemas.contract.user_schema import UserCreate
from taskflow.app.services.user_service import get_user_by_id as get_user_id
from taskflow.app.services.user_service import create_user, hash_pwd
from taskflow.app.services.user_service import update_user, delete_user, get_users, create_user
from taskflow.app.services.auth_service import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", status_code=status.HTTP_200_OK, )
def list_users(conn = Depends(get_db)):
    return get_users(conn)

@router.get("/me")
def read_me(current_user = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int):
    return get_user_id(user_id)

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_user(user: UserCreate):
    return create_user(
        username=user.username,
        email=user.email,
        password_hash = hash_pwd(user.password)
    )

@router.put("/{user_id}", status_code=status.HTTP_200_OK)
def edit_user(user_id: int, username: str, email: str):
    return update_user(user_id, username, email)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(user_id: int):
    return delete_user(user_id)