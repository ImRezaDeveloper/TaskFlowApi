from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from fastapi import APIRouter
from app.db.database import get_db
from app.models.users import User
from app.schemas.contract.token_schema import Token, RefreshRequest
from app.security.auth.jwt_handler import verify_refresh_token
from app.services.auth_service import authenticate_user
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=['auth'], prefix='/auth')

@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    return authenticate_user(
        email=form_data.username,
        password=form_data.password,
        db=db
    )

@router.post("/refresh", response_model=Token)
def refresh_token(data: RefreshRequest, conn = Depends(get_db)):
    return verify_refresh_token(data, conn)