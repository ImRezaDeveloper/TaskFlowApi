from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.taskflow.core.loggin import logger
from src.taskflow.crud.board_repository import (
    create_board_db,
    create_task_db,
    delete_board_db,
    delete_task_by_id_in_board_db,
    get_all_boards_db,
    get_all_tasks_by_id_in_board_db,
    get_board_by_id_db,
    get_board_by_name_db,
    get_task_by_id_in_board_db,
    update_board_db,
)
from src.taskflow.exceptions.board import (
    BoardAlreadyExistError,
    BoardCreationError,
    BoardNotFoundError,
    BoardPermissionDenied,
)
from src.taskflow.exceptions.task import TaskNotFoundError, TasksOfBoardsNotFound
from src.taskflow.exceptions.user import UserMustBeLoggedIn
from src.taskflow.models.boards import Board
from src.taskflow.models.tasks import Task
from src.taskflow.schemas.contract.board_schema import BoardUpdate


async def create_board_service(db, board_data, current_user_id: UUID):
    logger.info("create_board_started", board_name=str(board_data.name))

    try:
        if not current_user_id:
            raise UserMustBeLoggedIn(current_user_id)

        board = Board(
            name=board_data.name,
            description=board_data.description,
            owner_id=current_user_id,
        )

        existing_board = await get_board_by_name_db(db, board.name, current_user_id)

        if existing_board:
            raise BoardAlreadyExistError(board.name, current_user_id)

        created_board = await create_board_db(db, board)

        logger.info(
            "create_board",
            board_id=created_board.id,
        )

        return created_board
    except (BoardCreationError, BoardAlreadyExistError):
        raise
    except Exception as e:
        logger.error(
            "create_board_error",
            user_id=str(current_user_id),
            error=str(e),
            exc_info=True,
        )
        raise BoardCreationError(str(e))


async def get_all_boards_service(db, current_user_id: UUID):
    logger.info("get_all_boards_started", current_user_id=str(current_user_id))

    boards = await get_all_boards_db(db, current_user_id)

    logger.info("get_all_boards", current_user_id=str(current_user_id))

    return boards


async def get_board_by_id_service(db, board_id: UUID, current_user_id: UUID):
    logger.info(
        "get_board_by_id_started",
        board_id=str(board_id),
        current_user_id=str(current_user_id),
    )

    board = await get_board_by_id_db(db, board_id, current_user_id)

    if board is None:
        logger.warning(
            "get_board_by_id_failed", board_id=str(board_id), reason="board_not_found"
        )

        raise BoardNotFoundError(board_id)

    if board.owner_id != current_user_id:
        logger.warning(
            "get_board_by_id_failed",
            board_owner_id=str(board.owner_id),
            current_user_id=str(current_user_id),
            reason="unauthorized access",
        )

        owner_id = board.owner_id
        raise BoardPermissionDenied(owner_id)

    logger.info("get_board_by_id", board_id=str(board_id), action="success")

    return board


async def update_board_service(
    db: AsyncSession,
    board_id: UUID,
    board_data: BoardUpdate,
    current_user_id: UUID,
):
    logger.info(
        "update_board",
        board_id=str(board_id),
        board_data=list(board_data.model_dump(exclude_unset=True).keys()),
        current_user_id=str(current_user_id),
    )

    board = await get_board_by_id_db(db, board_id, current_user_id)

    if board is None:
        logger.warning(
            "update_board_failed",
            board_id=str(board_id),
            current_user_id=str(current_user_id),
            reason="board_not_found",
        )

        raise BoardNotFoundError(board_id)

    if board.owner_id != current_user_id:
        logger.warning(
            "update_board_failed",
            board_id=str(board_id),
            current_user_id=str(current_user_id),
            board_owner_id=str(board.owner_id),
            reason="unauthorized_update_attempt",
        )

        owner_id = board.owner_id
        raise BoardPermissionDenied(owner_id)

    logger.debug(
        "Update data for board %s: %s",
        board_id,
        board_data.model_dump(exclude_unset=True),
    )
    logger.debug(
        "update_data_for_specific_board",
        board_id=str(board_id),
        board_data=list(board_data.model_dump(exclude_unset=True).keys()),
    )

    updated_board = await update_board_db(db, board, board_data)

    logger.info(
        "update_board",
        board_id=str(board_id),
        current_user_id=str(current_user_id),
        action="success",
    )

    return updated_board


async def delete_board_service(db: AsyncSession, board_id: UUID, current_user_id: UUID):
    logger.info(
        "delete_board_by_id_started",
        board_id=str(board_id),
        current_user_id=str(current_user_id),
    )

    board = await get_board_by_id_db(db, board_id, current_user_id)

    if board is None:
        logger.warning(
            "delete_board_failed",
            board_id=str(board_id),
            current_user_id=str(current_user_id),
            reason="board_not_found",
        )

        raise BoardNotFoundError(board_id)

    if board.owner_id != current_user_id:
        logger.warning(
            "delete_board_failed",
            board_id=str(board_id),
            current_user_id=str(current_user_id),
            board_owner_id=str(board.owner_id),
            reason="unauthorized_delete_attempt",
        )

        owner_id = board.owner_id
        raise BoardPermissionDenied(owner_id)

    deleted_board = await delete_board_db(db, board)

    logger.info(
        "delete_board",
        board_id=str(board_id),
        current_user_id=str(current_user_id),
        action="success",
    )

    return deleted_board


async def create_task_service_board(
    db,
    board_id: UUID,
    task_data,
    current_user_id: UUID,
):
    logger.info(
        "create_task_in_board_started",
        user_id=str(current_user_id),
        board_id=str(board_id),
        title=task_data.title,
    )

    board = await get_board_by_id_db(db, board_id, current_user_id)

    if board is None:
        logger.warning(
            "create_task_in_board_failed",
            user_id=str(current_user_id),
            board_id=str(board_id),
            reason="board_not_found",
        )

        raise BoardNotFoundError(board_id)

    if board.owner_id != current_user_id:
        logger.warning(
            "create_task_in_board_failed",
            user_id=str(current_user_id),
            board_id=str(board_id),
            board_owner_id=str(board.owner_id),
            reason="unauthorized",
        )

        owner_id = board.owner_id
        raise BoardPermissionDenied(owner_id)

    task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        due_date=task_data.due_date,
        user_id=current_user_id,
        board_id=board.id,
    )

    created_task = await create_task_db(db, task)

    logger.info(
        "create_task_in_board_success",
        task_id=str(created_task.id),
        board_id=str(board_id),
        user_id=str(current_user_id),
        title=task_data.title,
    )

    return created_task


async def get_tasks_by_board_id_service(
    db: AsyncSession,
    board_id: UUID,
    current_user_id: UUID,
):
    logger.info(
        "get_tasks_in_board_started",
        user_id=str(current_user_id),
        board_id=str(board_id),
    )

    try:
        board = await get_board_by_id_db(db, board_id, current_user_id)

        if board is None:
            logger.warning(
                "get_tasks_in_board_failed",
                user_id=str(current_user_id),
                board_id=str(board_id),
                reason="board_not_found",
            )

            raise BoardNotFoundError(board_id)

        if board.owner_id != current_user_id:
            logger.warning(
                "get_tasks_in_board_failed",
                user_id=str(current_user_id),
                board_id=str(board_id),
                board_owner_id=str(board.owner_id),
                reason="unauthorized",
            )

            owner_id = board.owner_id
            raise BoardPermissionDenied(owner_id)

        tasks = await get_all_tasks_by_id_in_board_db(db, board_id)
        print(tasks)

        if not tasks:
            logger.warning(
                "get_tasks_in_board_failed",
                user_id=str(current_user_id),
                board_id=str(board_id),
                board_owner_id=str(board.owner_id),
                reason="unauthorized",
            )

            raise TasksOfBoardsNotFound(board_id)

        logger.info(
            "get_tasks_in_board_success",
            user_id=str(current_user_id),
            board_id=str(board_id),
            task_count=len(tasks),
        )

        return tasks
    except (
        TaskNotFoundError,
        TasksOfBoardsNotFound,
        BoardNotFoundError,
        BoardPermissionDenied,
    ):
        raise
    except Exception:
        logger.error()


async def delete_task_by_id_board_service(
    db: AsyncSession,
    board_id: UUID,
    task_id: UUID,
    current_user_id: UUID,
):
    logger.info(
        "delete_task_in_board_started",
        user_id=str(current_user_id),
        board_id=str(board_id),
        task_id=str(task_id),
    )

    board = await get_board_by_id_db(db, board_id, current_user_id)

    if board is None:
        logger.warning(
            "delete_task_in_board_failed",
            user_id=str(current_user_id),
            board_id=str(board_id),
            task_id=str(task_id),
            reason="board_not_found",
        )

        raise BoardNotFoundError(board_id)

    if board.owner_id != current_user_id:
        logger.warning(
            "delete_task_in_board_failed",
            user_id=str(current_user_id),
            board_id=str(board_id),
            task_id=str(task_id),
            board_owner_id=str(board.owner_id),
            reason="unauthorized",
        )

        owner_id = board.owner_id
        raise BoardPermissionDenied(owner_id)

    task = await get_task_by_id_in_board_db(db, board_id, task_id)

    if task is None:
        logger.warning(
            "delete_task_in_board_failed",
            user_id=str(current_user_id),
            board_id=str(board_id),
            task_id=str(task_id),
            reason="task_not_found",
        )

        raise TaskNotFoundError(task_id)

    await delete_task_by_id_in_board_db(db, board_id, task_id, current_user_id)

    logger.info(
        "delete_task_in_board_success",
        user_id=str(current_user_id),
        board_id=str(board_id),
        task_id=str(task_id),
    )

    return {"message": "Task deleted successfully"}
