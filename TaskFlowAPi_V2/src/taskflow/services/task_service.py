from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.taskflow.core.loggin import logger
from src.taskflow.crud.task_repository import (
    create_task_db,
    delete_task_db,
    get_board_tasks_db,
    get_task_by_id_db,
    update_task_db,
)
from src.taskflow.exceptions.task import (
    TaskCreationError,
    TaskDeleteError,
    TaskNotFoundAllError,
    TaskNotFoundError,
    TaskPermissionDenied,
    TasksOfBoardsNotFound,
    TaskUpdateError,
)
from src.taskflow.models.tasks import Task
from src.taskflow.schemas.contract.task_schema import TaskCreate, TaskUpdate


async def create_task_service(
    db: AsyncSession,
    task_data: TaskCreate,
    current_user_id: UUID,
) -> Task:

    logger.info(
        "create_task_started",
        user_id=str(current_user_id),
        board_id=str(task_data.board_id),
        title=task_data.title,
    )

    try:
        new_task = await create_task_db(db, task_data, current_user_id)

        logger.info(
            "create_task_success",
            task_id=str(new_task.id),
            user_id=str(current_user_id),
            board_id=str(task_data.board_id),
            title=task_data.title,
        )

        return new_task

    except TaskCreationError:
        raise

    except Exception as e:
        logger.error(
            "create_task_error",
            user_id=str(current_user_id),
            board_id=str(task_data.board_id),
            title=task_data.title,
            error=str(e),
        )
        raise TaskCreationError(str(e))


async def get_task_by_id_service(
    db: AsyncSession, task_id: UUID, current_user_id: UUID
) -> Task:

    logger.info(
        "get_task_started",
        task_id=str(task_id),
    )

    try:
        task = await get_task_by_id_db(db, task_id)

        if not task:
            logger.warning(
                "get_task_failed", task_id=str(task_id), reason="task_not_found"
            )
            raise TaskNotFoundError(task_id)

        if task.user_id != current_user_id:
            logger.warning(
                "get_task_failed",
                current_user_id=str(current_user_id),
                task_id=str(task_id),
                reason="unauthorized_access_attempt",
            )
            raise TaskPermissionDenied(task.user_id)

        return task
    except (TaskNotFoundError, TaskPermissionDenied):
        raise

    except Exception as e:
        logger.error(
            "create_task_error",
            task_id=str(task_id),
            user_id=str(current_user_id),
            error=str(e),
        )

        raise TaskCreationError(str(e))


async def get_board_tasks_service(
    db: AsyncSession,
    board_id: UUID,
    current_user_id: UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[Task]:
    logger.info("get_board_tasks_started", board_id=str(board_id), limit=str(limit))

    try:
        tasks = await get_board_tasks_db(db, board_id, skip, limit)

        if not tasks:
            logger.warning(
                "get_board_tasks_failed",
                board_id=str(board_id),
                skip=str(skip),
                limit=str(limit),
                reason="there is no task in a board",
            )
            raise TasksOfBoardsNotFound(board_id, skip, limit)

        logger.info(
            "get_board_tasks_success",
            board_id=str(board_id),
            skip=str(skip),
            limit=str(limit),
        )

        return tasks

    except TasksOfBoardsNotFound:
        raise

    except Exception as e:
        logger.error(
            "get_board_tasks_error", board_id=str(board_id), error=str(e), exc_info=True
        )
        raise TaskNotFoundAllError(tasks)


async def update_task_service(
    db: AsyncSession, task_id: UUID, update_data: TaskUpdate, current_user_id: UUID
) -> Task:
    logger.info(
        "update_task_started",
        task_id=str(task_id),
        update_fields=list(update_data.model_dump(exclude_unset=True).keys()),
    )

    try:
        task = await get_task_by_id_service(db, task_id, current_user_id)
        if not task:
            logger.warning(
                "get_task_failed", task_id=str(task_id), reason="task_not_found"
            )
            raise TaskNotFoundError(task_id)

        if task.user_id != current_user_id:
            logger.warning(
                "get_task_failed",
                current_user_id=str(current_user_id),
                task_id=str(task_id),
                reason="unauthorized_access_attempt",
            )

            raise TaskPermissionDenied(task.user_id)

        updated_task = await update_task_db(db, task.id, update_data)
        if updated_task is None:
            logger.error(
                "update_task_failed", task_id=str(task_id), reason="db_update_failed"
            )
            raise TaskUpdateError(task_id, "Database update operation failed")
        logger.info(
            "update_task_success",
            task_id=str(task_id),
            update_fields=list(update_data.model_dump(exclude_unset=True).keys()),
        )
        return updated_task

    except (TaskNotFoundError, TaskUpdateError):
        raise
    except Exception as e:
        logger.error(
            "update_task_error", task_id=str(task_id), error=str(e), exc_info=True
        )

        raise TaskUpdateError(task_id, str(e))


async def delete_task_service(
    db: AsyncSession, task_id: UUID, current_user_id: UUID
) -> bool:
    logger.info(
        "delete_task_started",
        task_id=str(task_id),
    )

    try:
        task = await get_task_by_id_service(db, task_id, current_user_id)

        if not task:
            logger.warning(
                "delete_task_failed", task_id=str(task_id), reason="task_not_found"
            )
            raise TaskNotFoundError(task_id)

        if task.user_id != current_user_id:
            logger.warning(
                "get_task_failed",
                current_user_id=str(current_user_id),
                task_id=str(task_id),
                reason="unauthorized_access_attempt",
            )

            raise TaskPermissionDenied(task.user_id)

        logger.info(
            "delete_task_success",
            task_id=str(task_id),
        )
        return await delete_task_db(db, task_id)
    except (TaskNotFoundError, TaskPermissionDenied):
        raise
    except Exception as e:
        logger.error(
            "update_task_error", task_id=str(task_id), error=str(e), exc_info=True
        )

        raise TaskDeleteError(task_id, str(e))