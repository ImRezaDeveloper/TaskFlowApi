from uuid import UUID
from fastapi import Depends, FastAPI, HTTPException
from starlette import status
from src.taskflow.core.loggin import logger
from src.taskflow.core.security import hash_pwd
from src.taskflow.crud.user_repository import get_user_by_id as get_user_id
from src.taskflow.crud.user_repository import create_user_db, update_user_db, get_users_db, delete_user_db
from src.taskflow.db.database import get_db
from src.taskflow.models.users import User
from src.taskflow.schemas.contract.user_schema import UserUpdate
from ..validators import validate_email_availability
from sqlalchemy.ext.asyncio import AsyncSession

def get_users(db: AsyncSession):
    users = get_users_db(db)
    return users

async def get_user_by_id(user_id: UUID, db: AsyncSession, current_user_id) -> User:
    logger.info(
        "get_user_by_id_started",
        user_id=str(user_id)
    )

    existing_user = await get_user_id(db, user_id)
    
    if not existing_user:
        logger.warning(
            "get_user_by_id_failed",
            reason="user_not_found"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    logger.info(
        "get_user_by_id",
        user_id=str(user_id),
        status="success"
    )
    
    return existing_user
    
async def create_user(
    username: str,
    email: str,
    hashed_password: str,
    full_name: str,
    is_active: bool,
    is_verified: bool,
    db: AsyncSession,
):
    logger.info(
        "create_user_started",
        username=username,
        email=email,
        full_name=full_name,
        is_active=is_active,
        is_verified=is_verified
    )

    try:
        new_user = await create_user_db(
            username,
            email,
            hashed_password,
            full_name,
            is_active,
            is_verified,
            db
        )

        logger.info(
            "create_user_success",
            user_id=str(new_user.id),
            username=username,
            email=email
        )

        return new_user

    except Exception as e:
        logger.error(
            "create_user_error",
            username=username,
            email=email,
            error=str(e)
        )
        raise

async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: AsyncSession,
):
    logger.info(
        "update_user_started",
        user_id=str(user_id),
        update_fields=list(user_data.model_dump(exclude_unset=True).keys())
    )

    user = await get_user_by_id(user_id, db)

    if not user:
        logger.warning(
            "update_user_failed",
            user_id=str(user_id),
            reason="user_not_found"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    updated_user = await update_user_db(db, user, user_data)

    logger.info(
        "update_user_success",
        user_id=str(user_id),
        updated_fields=list(user_data.model_dump(exclude_unset=True).keys())
    )

    return updated_user

async def delete_user(
    user_id: UUID,
    db: AsyncSession,
):
    logger.info(
        "delete_user_started",
        user_id=str(user_id)
    )

    user = await get_user_by_id(user_id, db)

    if not user:
        logger.warning(
            "delete_user_failed",
            user_id=str(user_id),
            reason="user_not_found"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    deleted_user = await delete_user_db(db, user_id)

    logger.info(
        "delete_user_success",
        user_id=str(user_id)
    )

    return deleted_user