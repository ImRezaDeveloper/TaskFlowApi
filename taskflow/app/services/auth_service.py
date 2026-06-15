from fastapi import Depends, HTTPException
from taskflow.app.core.security import verify_pwd
from taskflow.app.security.auth.jwt_handler import create_access_token
from taskflow.app.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from taskflow.app.security.auth.oauth2 import oauth_schemes
from taskflow.app.api.dependencies import get_db

oauth = oauth_schemes


def authenticate_user(email, password, conn = Depends(get_db)):
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, email, password_hash
        FROM users
        WHERE email = %s
        """,
        (email,)
    )

    user = cur.fetchone()

    cur.close()
    # conn.close()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Wrong email or password"
        )

    user_id, email, password_hash = user

    if not verify_pwd(
        plainPassword=password,
        hashedPassword=password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Wrong email or password"
        )

    # if not is_active:
    #     raise HTTPException(
    #         status_code=403,
    #         detail="Inactive user"
    #     )

    access_token = create_access_token(
        data={"sub": str(user_id)}
    )

    return {
        "access_token": access_token,
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