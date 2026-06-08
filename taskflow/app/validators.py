from fastapi import HTTPException, status
from taskflow.app.crud.user_repository import get_user_by_email

def validate_email_availability(email: str):
    existing_user = get_user_by_email(email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    return True