from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from taskflow.app.users.user_router import router
from passlib.context import CryptContext

# psw
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(
    title="TaskFlow API",
    description="Production-ready team task management API",
    version="1.0.0"
)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)