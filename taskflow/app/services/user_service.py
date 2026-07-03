import logging
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from starlette import status
from taskflow.app.core.security import hash_pwd
from taskflow.app.crud.user_repository import get_user_by_id as get_user_id
from taskflow.app.crud.user_repository import create_user_db, update_user_db, get_users_db
from taskflow.app.db.database import get_db
from taskflow.app.models.users import User
from ..validators import validate_email_availability
logger = logging.getLogger("taskflow.services.tasks")
from sqlalchemy.ext.asyncio import AsyncSession

def get_users(db: AsyncSession = Depends(get_db)):
    users = get_users_db(db)
    return users

def get_user_by_id(user_id: UUID, current_user_id: UUID,db: AsyncSession = Depends(get_db)) -> User:
    logger.info(f"User {current_user_id} requested Uesr ID {user_id}")
    
    existing_user = get_user_id(db, user_id)
    
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    return existing_user
    
def create_user(username: str, email: str, hashed_password: str, full_name: str, is_active: bool, is_verified: bool, get_db):
    
    # validate_email_availability(email, get_db)
    hash_pwd(hashed_password)
    return create_user_db(username, email, hashed_password, full_name, is_active, is_verified, get_db)

def update_user(user_id: UUID, username, email):
    user = get_user_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    return update_user_db(user_id, username, email)

def delete_user(user_id: UUID, user):
    
    user = get_user_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    return 