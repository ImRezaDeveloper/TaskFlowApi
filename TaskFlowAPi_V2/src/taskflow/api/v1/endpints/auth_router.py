from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.taskflow.db.database import get_db
from src.taskflow.schemas.contract.token_schema import RefreshRequest, Token
from src.taskflow.security.auth.jwt_handler import verify_refresh_token
from src.taskflow.services.auth_service import authenticate_user

router = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    return await authenticate_user(
        email=form_data.username, password=form_data.password, db=db
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(data: RefreshRequest, conn=Depends(get_db)):
    return await verify_refresh_token(data, conn)
