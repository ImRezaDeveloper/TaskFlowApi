from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.taskflow.exceptions.auth_user import (
    CouldNotValidateCredentialsError,
    EmailorPasswordWrongError,
)
from src.taskflow.exceptions.board import (
    BoardNotFoundError,
    BoardCreationError,
    BoardPermissionDenied,
    BoardAlreadyExistError,
)
from src.taskflow.exceptions.task import (
    TaskNotFoundError,
    TaskPermissionDenied,
    TaskCreationError,
    TaskDeleteError,
    TasksOfBoardsNotFound,
    TaskNotFoundAllError,
    TaskUpdateError,
)


# board
async def board_not_found_handler(request: Request, exc: BoardNotFoundError):

    return JSONResponse(status_code=404, content={"detail": str(exc)})


async def permission_deneid_board_handler(request: Request, exc: BoardPermissionDenied):

    return JSONResponse(status_code=403, content={"detail": str(exc)})


async def board_creation_handler(request: Request, exc: BoardCreationError):

    return JSONResponse(content={"detail": str(exc)})


async def board_already_exist_handler(request: Request, exc: BoardAlreadyExistError):

    return JSONResponse(status_code=409, content={"detail": str(exc)})


async def task_not_found_all_error_handler(request: Request, exc: TaskNotFoundAllError):

    return JSONResponse(content={"detail": str(exc)})


async def task_of_board_not_found_handler(request: Request, exc: TasksOfBoardsNotFound):

    return JSONResponse(status_code=404, content={"detail": str(exc)})


# tasks
async def task_not_found_handler(request: Request, exc: TaskNotFoundError):

    return JSONResponse(status_code=404, content={"detail": str(exc)})


async def permission_deneid_task_handler(request: Request, exc: TaskPermissionDenied):

    return JSONResponse(status_code=403, content={"detail": str(exc)})


async def task_creation_error_handler(request: Request, exc: TaskCreationError):

    return JSONResponse(content={"detail": str(exc)})


async def task_delete_error_handler(request: Request, exc: TaskDeleteError):

    return JSONResponse(status_code=201, content={"detail": str(exc)})


async def task_update_error_handler(request: Request, exc: TaskUpdateError):

    return JSONResponse(status_code=500, content={"detail": str(exc)})


# auth_user
async def email_or_password_wrong_handler(
    request: Request, exc: EmailorPasswordWrongError
):

    return JSONResponse(status_code=401, content={"detail": "email or password wrong!"})


async def could_not_validate_credentials_error_handler(
    request: Request, exc: CouldNotValidateCredentialsError
):

    return JSONResponse(
        status_code=401, content={"detail": "Could not validate credentials!"}
    )


def register_exception_handlers(app: FastAPI):

    app.add_exception_handler(
        BoardNotFoundError,
        board_not_found_handler,
    )
    app.add_exception_handler(BoardPermissionDenied, permission_deneid_board_handler)
    app.add_exception_handler(BoardCreationError, board_creation_handler)
    app.add_exception_handler(BoardAlreadyExistError, board_already_exist_handler)
    app.add_exception_handler(TaskNotFoundAllError, task_not_found_all_error_handler)
    app.add_exception_handler(TaskPermissionDenied, permission_deneid_task_handler)
    app.add_exception_handler(TaskNotFoundError, task_not_found_handler)
    app.add_exception_handler(TaskCreationError, task_creation_error_handler)
    app.add_exception_handler(TaskDeleteError, task_delete_error_handler)
    app.add_exception_handler(TaskUpdateError, task_update_error_handler)
    app.add_exception_handler(
        EmailorPasswordWrongError, email_or_password_wrong_handler
    )
    app.add_exception_handler(
        CouldNotValidateCredentialsError, could_not_validate_credentials_error_handler
    )
