from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.taskflow.exceptions.board import BoardNotFoundError, BoardCreationError, BoardPermissionDenied, BoardAlreadyExistError
from src.taskflow.exceptions.task import TaskNotFoundError


async def board_not_found_handler(request: Request, exc: BoardNotFoundError):

    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc)
        }
    )

async def permission_deneid_board_handler(request: Request, exc: BoardPermissionDenied):

    return JSONResponse(
        status_code=403,
        content={
            "detail": str(exc)
        }
    )

async def board_creation_handler(request: Request, exc: BoardCreationError):

    return JSONResponse(
        content={
            "detail": str(exc)
        }
    )

async def board_already_exist_handler(request: Request, exc: BoardAlreadyExistError):

    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exc)
        }
    )

async def task_not_found_handler(request: Request, exc: TaskNotFoundError):

    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc)
        }
    )

def register_exception_handlers(app: FastAPI):

    app.add_exception_handler(
        BoardNotFoundError,
        board_not_found_handler,
    )
    app.add_exception_handler(
        TaskNotFoundError,
        task_not_found_handler
    )
    app.add_exception_handler(
        BoardPermissionDenied,
        permission_deneid_board_handler
    )
    app.add_exception_handler(
        BoardCreationError,
        board_creation_handler
    )
    app.add_exception_handler(
        BoardAlreadyExistError,
        board_already_exist_handler
    )