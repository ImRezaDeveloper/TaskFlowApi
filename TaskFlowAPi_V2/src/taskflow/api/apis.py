# for include routing
from fastapi import FastAPI

from taskflow.src.taskflow.api.v1.endpints.user_router import router
from taskflow.src.taskflow.api.v1.endpints.auth_router import router
from taskflow.src.taskflow.api.v1.endpints.task_router import router
from taskflow.src.taskflow.api.v1.endpints.board_router import router
from taskflow.src.taskflow.api.v1.endpints.comment_router import router


def get_routes():
    app = FastAPI()

    src.taskflow.include_router(router)