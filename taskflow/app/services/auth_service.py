from fastapi import Depends, HTTPException
from taskflow.app.core.security import verify_pwd
from taskflow.app.security.auth.jwt_handler import create_access_token, create_refresh_token
from taskflow.app.core.config import settings
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from taskflow.app.security.auth.oauth2 import oauth_schemes
from taskflow.app.api.dependencies import get_db
from psycopg2.extras import RealDictCursor

oauth = oauth_schemes

# this method should be use Redis for set rate limitions ===
def authenticate_user(email: str, password: str, conn = Depends(get_db)):
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        
        cur.execute(
            "SELECT id, email, password_hash FROM users WHERE email = %s",
            (email,)
        )
        user = cur.fetchone()

        if not user or not verify_pwd(password, user["password_hash"]):
            raise HTTPException(
                status_code=401,
                detail="Wrong email or password"
            )

        user_id = user["id"]
        access_token = create_access_token(data={"sub": str(user_id)})
        refresh_token = create_refresh_token(data={"sub": str(user_id)})
        
        cur.execute(
            "INSERT INTO refresh_tokens (user_id, token) VALUES (%s, %s)", 
            (user_id, refresh_token)
        )
        
        conn.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# get current user
def get_current_user(
    token: str = Depends(oauth),
    conn = Depends(get_db)
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

    cur = conn.cursor()
    
    cur.execute(
        """
        SELECT id, username, email, role_id
        FROM users
        WHERE id = %s
        """,
        (user_id,)
    )

    user = cur.fetchone()
    
    cur.close()

    if user is None:
        raise credentials_exception

    # if not is_active:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Inactive user"
    #     )
    
    user_id, username, email, role_id = user

    return {
        "id": user_id,
        "username": username,
        "email": email,
        "role_id": role_id
    }