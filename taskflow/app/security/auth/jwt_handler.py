from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException
from app.core.config import settings
from taskflow.app.schema.user_schema import TokenData
from jose import jwt, JWTError

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = int(payload["sub"])
        if user_id is None:
            raise HTTPException(status_code=401, detail="Could not verify Credentials", headers={"WWW-Authenticate": "Bearer"})
        return TokenData(user_id=user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not verify Credentials", headers={"WWW-Authenticate": "Bearer"})