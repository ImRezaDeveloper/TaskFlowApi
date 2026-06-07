from fastapi import FastAPI, HTTPException
from starlette import status
from taskflow.app.core.security import hash_password
from taskflow.app.users.user_repository import get_user_by_id as get_user_id
from taskflow.app.users.user_repository import create_user_db
from taskflow.app.users.user_schema import UserCreate
from .validators import validate_email_availability
from pwdlib import PasswordHash

# password hashing
password_hash = PasswordHash.recommended()

def get_user_by_id(user_id: int):
    
    existing_user = get_user_id(user_id)
    
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    return existing_user

# def hash_password_email_validation(user: UserCreate):
    
#     hashed_password = hash_password(user.password)
    
#     validate_email_availability(user.email)

def hash_password(plainPassword: str):
    return password_hash.hash(plainPassword)
    

def create_user(username: str, email: str, password_hash: str):
    
    return create_user_db(username, email, password_hash)