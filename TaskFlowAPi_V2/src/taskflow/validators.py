from fastapi import HTTPException, status
from src.taskflow.crud.user_repository import get_user_by_email

def validate_email_availability(email: str, get_db):
    existing_user = get_user_by_email(email, get_db)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    return True