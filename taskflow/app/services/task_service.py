import logging
from uuid import UUID
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from taskflow.app.crud.task_repository import (
    create_task_db,
    get_task_by_id_db,
    get_board_tasks_db,
    update_task_db,
    delete_task_db
)
from taskflow.app.schemas.contract.task_schema import TaskCreate, TaskUpdate
from taskflow.app.models.tasks import Task

logger = logging.getLogger("taskflow.services.tasks")


def create_task_service(db: AsyncSession, task_data: TaskCreate, current_user_id: UUID) -> Task:
    # logger.info(f"User {current_user_id} is attempting to create a task in board {task_data.board_id}")
    try:
        new_task = create_task_db(db, task_data, current_user_id)
        logger.info(f"Task successfully created with ID {new_task.id} by user {current_user_id}")
        return new_task
    except Exception as e:
        logger.error(f"Failed to create task for user {current_user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="there was an error in creating task"
        )


def get_task_by_id_service(db: AsyncSession, task_id: UUID, current_user_id: UUID) -> Task:
    logger.info(f"User {current_user_id} requested task ID {task_id}")
    
    task = get_task_by_id_db(db, task_id)
    
    if not task:
        logger.warning(f"Task ID {task_id} not found in database.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="your current task not found!"
        )
        
    if task.user_id != current_user_id:
        logger.warning(f"Unauthorized access attempt! User {current_user_id} tried to view task {task_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you don't have permission to do this!"
        )
        
    return task

async def get_board_tasks_service(db: AsyncSession, board_id: UUID, current_user_id: UUID, skip: int = 0, limit: int = 100) -> List[Task]:
    logger.info(f"User {current_user_id} fetching tasks for board {board_id} with limit={limit}")
    try:
        tasks = await get_board_tasks_db(db, board_id, skip, limit)
        return tasks
    except Exception as e:
        logger.error(f"Error fetching tasks for board {board_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="there was an error to get all tasks"
        )


def update_task_service(db: AsyncSession, task_id: UUID, update_data: TaskUpdate, current_user_id: UUID) -> Task:
    logger.info(f"User {current_user_id} attempting to update task {task_id}")
    
    get_task_by_id_service(db, task_id, current_user_id)
    
    try:
        updated_task = update_task_db(db, task_id, update_data)
        logger.info(f"Task {task_id} successfully updated by user {current_user_id}")
        return updated_task
    except Exception as e:
        logger.error(f"Error updating task {task_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="there was an error to update task"
        )


def delete_task_service(db: AsyncSession, task_id: UUID, current_user_id: UUID) -> bool:
    logger.info(f"User {current_user_id} attempting to delete task {task_id}")
    
    get_task_by_id_service(db, task_id, current_user_id)
    
    try:
        delete_task_db(db, task_id)
        logger.info(f"Task {task_id} successfully deleted by user {current_user_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="there was an error to deleting task"
        )