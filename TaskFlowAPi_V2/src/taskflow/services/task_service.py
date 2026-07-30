from src.taskflow.core.loggin import logger
from uuid import UUID
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.taskflow.crud.task_repository import (
    create_task_db,
    get_task_by_id_db,
    get_board_tasks_db,
    update_task_db,
    delete_task_db
)
from src.taskflow.schemas.contract.task_schema import TaskCreate, TaskUpdate
from src.taskflow.models.tasks import Task


async def create_task_service(
    db: AsyncSession,
    task_data: TaskCreate,
    current_user_id: UUID,
) -> Task:
    logger.info(
        "create_task_started",
        user_id=str(current_user_id),
        board_id=str(task_data.board_id),
        title=task_data.title
    )

    try:
        new_task = await create_task_db(db, task_data, current_user_id)

        logger.info(
            "create_task_success",
            task_id=str(new_task.id),
            user_id=str(current_user_id),
            board_id=str(task_data.board_id),
            title=task_data.title
        )

        return new_task

    except Exception as e:
        logger.error(
            "create_task_error",
            user_id=str(current_user_id),
            board_id=str(task_data.board_id),
            title=task_data.title,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="There was an error in creating task"
        )


async def get_task_by_id_service(db: AsyncSession, task_id: UUID, current_user_id: UUID) -> Task:
    logger.info(
        "get_task_started",
        task_id=str(task_id),
    )
    
    task = await get_task_by_id_db(db, task_id)
    
    if not task:
        logger.warning(
            "get_task_failed",
            task_id=str(task_id),
            reason="task_not_found"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="your current task not found!"
        )
        
    if task.user_id != current_user_id:
        logger.warning(
            "get_task_failed",
            current_user_id=str(current_user_id),
            task_id=str(task_id),
            reason="unauthorized_access_attempt"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you don't have permission to do this!"
        )
        
    return task

async def get_board_tasks_service(db: AsyncSession, board_id: UUID, current_user_id: UUID, skip: int = 0, limit: int = 100) -> List[Task]:
    logger.info(
        "get_board_tasks_started",
        board_id=str(board_id),
        limit=str(limit)
    )
    try:
        tasks = await get_board_tasks_db(db, board_id, skip, limit)

        logger.info(
            "get_board_tasks_success",
            board_id=str(board_id),
            skip=str(skip),
            limit=str(limit)
        )

        return tasks
    except Exception as e:
        logger.error(
            "get_board_tasks_error",
            board_id=str(board_id),
            error=str(e),
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="there was an error to get all tasks"
        )


async def update_task_service(db: AsyncSession, task_id: UUID, update_data: TaskUpdate, current_user_id: UUID) -> Task:
    logger.info(
        "update_task_started",
        task_id=str(task_id),
        update_fields=list(update_data.model_dump(exclude_unset=True).keys())
    )
    await get_task_by_id_service(db, task_id, current_user_id)
    
    try:
        updated_task = await update_task_db(db, task_id, update_data)
        logger.info(
            "update_task_success",
            task_id=str(task_id),
            update_fields=list(update_data.model_dump(exclude_unset=True).keys())
        )
        return updated_task
    except Exception as e:
        logger.error(
            "update_task_error",
            task_id=str(task_id),
            error=str(e),
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="there was an error to update task"
        )


async def delete_task_service(db: AsyncSession, task_id: UUID, current_user_id: UUID) -> bool:
    logger.info(
            "delete_task_started",
            task_id=str(task_id),
        )
    
    task = await get_task_by_id_service(db, task_id, current_user_id)

    if not task:
        logger.warning(
            "delete_task_failed",
            task_id=str(task_id),
            reason="task_not_found"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    logger.info(
        "delete_task_success",
        task_id=str(task_id),
    )
    return await delete_task_db(db, task_id)