from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from taskflow.app.core.config import Settings
from taskflow.app.api.v1.endpints.auth_router import router as auth_router
from taskflow.app.api.v1.endpints.user_router import router as user_router
from taskflow.app.api.v1.endpints.task_router import router as task_router
from taskflow.app.core.loggin import setup_logging
from taskflow.app.db.database import Base, engine

setup_logging()

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Task Management Api",
    description="Production-ready team task management API",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(task_router)

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