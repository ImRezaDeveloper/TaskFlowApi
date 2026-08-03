from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.taskflow.core.security import hash_pwd
from src.taskflow.db.database import get_db
from src.taskflow.schemas.contract.user_schema import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from src.taskflow.services.auth_service import get_current_user
from src.taskflow.services.user_service import (
    create_user,
    delete_user,
    get_users,
    # hash_pwd,
    update_user,
)
from src.taskflow.services.user_service import get_user_by_id as get_user_id

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await get_users(db)


@router.get("/me")
async def read_me(current_user=Depends(get_current_user)):
    return current_user


@router.get("/{user_id}")
async def get_user(
    user_id: UUID,
    get_db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await get_user_id(user_id, get_db, current_user)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_pwd(user_data.password),
        full_name=user_data.full_name,
        is_active=user_data.is_active,
        is_verified=user_data.is_verified,
        db=db,
    )


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def edit_user(
    user_id: UUID, user_data: UserUpdate, db: AsyncSession = Depends(get_db)
):
    return await update_user(user_id, user_data, db)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    return await delete_user(user_id, db)
