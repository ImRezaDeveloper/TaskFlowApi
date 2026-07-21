from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException
from src.taskflow.core.config import settings
from src.taskflow.schemas.contract.token_schema import TokenData
from jose import jwt, JWTError
from psycopg2.extras import RealDictCursor

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
    
def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=7))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_refresh_token(data: dict, db_connection):
    try:
        payload = jwt.decode(data.refresh_token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id:int = int(payload.get("sub"))
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Could not verify Credentials")
            
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid refresh token")

    with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
        
        cursor.execute("SELECT * FROM refresh_tokens WHERE token = %s", (data.refresh_token,))
        token_in_db = cursor.fetchone()
        
        if not token_in_db:
            raise HTTPException(status_code=403, detail="Refresh token not found")

        cursor.execute("SELECT id, email FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        new_access_token = create_access_token({"sub": str(user_id)})
        new_refresh_token = create_refresh_token({"sub": str(user_id)})
        
        cursor.execute("DELETE FROM refresh_tokens WHERE token = %s", (data.refresh_token,))
        
        cursor.execute(
            "INSERT INTO refresh_tokens (token, user_id) VALUES (%s, %s)",
            (new_refresh_token, user["id"])
        )
        
        db_connection.commit()

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }