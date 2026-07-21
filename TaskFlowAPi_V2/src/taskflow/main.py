from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.taskflow.core.config import Settings
from src.taskflow.api.v1.endpints.auth_router import router as auth_router
from src.taskflow.api.v1.endpints.user_router import router as user_router
from src.taskflow.api.v1.endpints.task_router import router as task_router
from src.taskflow.api.v1.endpints.board_router import router as board_router
from src.taskflow.api.v1.endpints.comment_router import router as comment_router
from src.taskflow.core.loggin import setup_logging
from src.taskflow.db.database import Base, engine

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Task Management Api",
    description="Production-ready team task management API",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(task_router)
app.include_router(board_router)
app.include_router(comment_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    import logging
    # Named logger for this specific module
    logger = logging.getLogger(__name__)
    logger.info("Root endpoint was hit!")
    # return {"message": f"Welcome to {Settings.PROJECT_NAME}!"}