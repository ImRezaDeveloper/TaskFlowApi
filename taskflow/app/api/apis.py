# for include routing
from fastapi import FastAPI

from taskflow.app.api.v1.endpints.user_router import router
from taskflow.app.api.v1.endpints.auth_router import router
from taskflow.app.api.v1.endpints.task_router import router


def get_routes():
    app = FastAPI()

    app.include_router(router)