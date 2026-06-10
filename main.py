from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from taskflow.app.core.config import Settings
from taskflow.app.api.apis import router


app = FastAPI(
    title="Task Management Api",
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