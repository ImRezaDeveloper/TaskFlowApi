from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from app.security.auth.hashing import hash_pwd, verify_pwd
from taskflow.app.core.jwt_handler import create_access_token
from app.core.config import settings
from app.dependencies import get_db
from app.schemas.user_schemas import Token, UserUpdate, UserDisplay
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from fastapi import APIRouter

router = APIRouter(tags=['auth'], prefix='/auth')


@router.post('/login', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = select(User).where(User.email == form_data.username)
    result = await db.execute(user)
    final = result.scalars().first()
    
    if not final:
        raise HTTPException(status_code=401, detail="Wrong email or password")

    if not verify_pwd(plainPassword=form_data.password, hashedPassword=final.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    if not final.is_active:
        raise HTTPException(status_code=404, detail="Inactive user")
    
    access_token_expire = timedelta(minutes=settings.TOKEN_EXPIRES)
    access_token = create_access_token(data={"sub": final.email}, expires_delta=access_token_expire)
    return {"access_token": access_token, "token_type": "bearer"}