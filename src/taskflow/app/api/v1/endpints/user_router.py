from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.contract.user_schema import  UserCreate, UserResponse
from app.services.user_service import get_user_by_id as get_user_id
from app.services.user_service import create_user, hash_pwd
from app.services.user_service import update_user, delete_user, get_users, create_user
from app.services.auth_service import get_current_user
from app.security.auth.auth_dependencies import require_admin
from app.schemas.contract.user_schema import UserResponse
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserResponse])
def list_users(db: AsyncSession = Depends(get_db)):
    return get_users(db)


@router.get("/me")
def read_me(current_user = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}")
def get_user(
    user_id: UUID,
    current_user = Depends(get_current_user),
    get_db: AsyncSession = Depends(get_db),
):
    return get_user_id(user_id, current_user, get_db)

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_user(user: UserCreate, get_db: AsyncSession = Depends(get_db)):
    return create_user(
        username=user.username,
        email=user.email,
        hashed_password = hash_pwd(user.hashed_password),
        full_name=user.full_name,
        is_active=user.is_active,
        is_verified=user.is_verified,
        get_db=get_db
    )

@router.put("/{user_id}", status_code=status.HTTP_200_OK)
def edit_user(user_id: int, username: str, email: str):
    return update_user(user_id, username, email)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(user_id: int, required_admin = Depends(require_admin)):
    return delete_user(user_id)