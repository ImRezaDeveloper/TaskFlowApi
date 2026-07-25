import logging
from uuid import UUID
from fastapi import Depends, FastAPI, HTTPException
from starlette import status
from src.taskflow.core.security import hash_pwd
from src.taskflow.crud.user_repository import get_user_by_id as get_user_id
from src.taskflow.crud.user_repository import create_user_db, update_user_db, get_users_db, delete_user_db
from src.taskflow.db.database import get_db
from src.taskflow.models.users import User
from src.taskflow.schemas.contract.user_schema import UserUpdate
from ..validators import validate_email_availability
logger = logging.getLogger("taskflow.services.users")
from sqlalchemy.ext.asyncio import AsyncSession

def get_users(db: AsyncSession):
    users = get_users_db(db)
    return users

async def get_user_by_id(user_id: UUID, db: AsyncSession) -> User:
    # logger.info(f"User {current_user_id} requested Uesr ID {user_id}")
    
    existing_user = await get_user_id(db, user_id)
    
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    return existing_user
    
async def create_user(username: str, email: str, hashed_password: str, full_name: str, is_active: bool, is_verified: bool, db: AsyncSession):
    
    # validate_email_availability(email, get_db)
    hash_pwd(hashed_password)
    return await create_user_db(username, email, hashed_password, full_name, is_active, is_verified, db)

async def update_user(user_id: UUID, user_data: UserUpdate, db: AsyncSession):
    user = await get_user_by_id(user_id, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    return await update_user_db(db, user, user_data)

async def delete_user(user_id: UUID, db: AsyncSession):
    
    user = await get_user_by_id(user_id, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    return await delete_user_db(db, user_id)