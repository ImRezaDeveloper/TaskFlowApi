from fastapi import Depends, HTTPException
from sqlalchemy import select
from src.taskflow.core.security import verify_pwd
from src.taskflow.models.users import User
from src.taskflow.security.auth.jwt_handler import create_access_token, create_refresh_token
from src.taskflow.core.config import settings
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from src.taskflow.security.auth.oauth2 import oauth_schemes
from src.taskflow.db.database import get_db
from psycopg2.extras import RealDictCursor
from sqlalchemy.ext.asyncio import AsyncSession
from src.taskflow.core.loggin import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

oauth = oauth_schemes

# this method should be use Redis for set rate limitions ===
async def authenticate_user(
    email: str,
    password: str,
    db: AsyncSession = Depends(get_db)
):
    logger.info(
        "Authentication started. email=%s",
        email
    )

    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        logger.warning(
            "Authentication failed. User not found. email=%s",
            email
        )

        raise HTTPException(
            status_code=401,
            detail="Wrong email or password"
        )

    if not verify_pwd(password, user.hashed_password):
        logger.warning(
            "Authentication failed. Invalid password. user_id=%s",
            user.id
        )

        raise HTTPException(
            status_code=401,
            detail="Wrong email or password"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )

    logger.info(
        "Authentication succeeded. user_id=%s",
        user.id
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

    

# get current user
async def get_current_user(
    token: str = Depends(oauth),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception

    return user