# from datetime import timedelta
# from fastapi.security import OAuth2PasswordRequestForm
# from taskflow.app.core.security import hash_pwd, verify_pwd
# from taskflow.app.security.auth.jwt_handler import create_access_token
# from taskflow.app.core.config import settings
# from taskflow.app.api.dependencies import get_db
# from taskflow.app.schemas.contract.token_schema import Token, TokenData
# # from taskflow. import User
# # from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi import Depends, HTTPException
# from fastapi import APIRouter
# from taskflow.app.crud.user_repository import verify_exists_user

# router = APIRouter(tags=['auth'], prefix='/auth')


# @router.post('/login', response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
#     user = verify_exists_user(email) # email
#     result = await db.execute(user)
#     final = result.scalars().first()
    
#     if not final:
#         raise HTTPException(status_code=401, detail="Wrong email or password")

#     if not verify_pwd(plainPassword=form_data.password, hashedPassword=final.password):
#         raise HTTPException(status_code=401, detail="Incorrect email or password")

#     if not final.is_active:
#         raise HTTPException(status_code=404, detail="Inactive user")
    
#     access_token_expire = timedelta(minutes=settings.TOKEN_EXPIRES)
#     access_token = create_access_token(data={"sub": final.email}, expires_delta=access_token_expire)
#     return {"access_token": access_token, "token_type": "bearer"}