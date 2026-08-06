from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.taskflow.crud.user_repository import get_user_by_email, get_user_by_id
from src.taskflow.exceptions.auth_user import (
    CouldNotValidateCredentialsError,
    EmailorPasswordWrongError,
)
from src.taskflow.core.config import settings
from src.taskflow.core.loggin import logger
from src.taskflow.core.security import verify_pwd
from src.taskflow.db.database import get_db
from src.taskflow.models.users import User
from src.taskflow.security.auth.jwt_handler import (
    create_access_token,
    create_refresh_token,
)
from src.taskflow.security.auth.oauth2 import oauth_schemes

oauth = oauth_schemes


# this method should be use Redis for set rate limitions ===
async def authenticate_user(
    email: str, password: str, db: AsyncSession = Depends(get_db)
):
    logger.info("authenticate_user_started", email=email)

    user = await get_user_by_email(db, email)

    if user is None:
        logger.warning("authenticate_user_failed", email=email, reason="user_not_found")

        # status=401
        raise EmailorPasswordWrongError(email, password)

    if not verify_pwd(password, user.hashed_password):
        logger.warning(
            "authenticate_user_failed",
            user_id=str(user.id),
            email=email,
            reason="invalid_password",
        )

        raise EmailorPasswordWrongError(email, password)

    access_token = create_access_token(data={"sub": str(user.id)})

    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    logger.info("authenticate_user_success", user_id=str(user.id), email=email)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# get current user
async def get_current_user(
    token: str = Depends(oauth), db: AsyncSession = Depends(get_db)
):

    logger.info(
        "get_current_user_started",
        token_preview=token[:10] + "..." if len(token) > 10 else token,
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            logger.warning("get_current_user_failed", reason="missing_user_id_in_token")
            raise CouldNotValidateCredentialsError
    except JWTError:
        raise CouldNotValidateCredentialsError()

    user = await get_user_by_id(db, user_id)

    if user is None:
        logger.warning(
            "get_current_user_failed", user_id=user_id, reason="user_not_found_in_db"
        )
        raise CouldNotValidateCredentialsError()

    logger.info("get_current_user_success", user_id=str(user.id), email=user.email)

    return user
