from fastapi import FastAPI, HTTPException
from starlette import status
from taskflow.app.core.security import hash_pwd
from taskflow.app.crud.user_repository import get_user_by_id as get_user_id
from taskflow.app.crud.user_repository import create_user_db, update_user_db, get_users_db
from ..validators import validate_email_availability

def get_users(conn):
    
    return get_users_db(conn)

def get_user_by_id(user_id: int, current_user, conn):
    
    existing_user = get_user_id(user_id, current_user, conn)
    
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    return existing_user
    
def create_user(username: str, email: str, password_hash: str, role_id, conn):
    
    validate_email_availability(email, conn)
    hash_pwd(password_hash)
    return create_user_db(username, email, password_hash, role_id, conn)

def update_user(user_id: int, username, email):
    user = get_user_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    return update_user_db(user_id, username, email)

def delete_user(user_id: int, user):
    
    user = get_user_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    return 