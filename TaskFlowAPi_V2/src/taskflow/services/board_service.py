from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from src.taskflow.crud.task_repository import delete_task_db
from src.taskflow.models.boards import Board
from src.taskflow.crud.board_repository import create_task_db, delete_task_by_id_in_board_db, get_task_by_id_in_board_db, update_board_db, delete_board_db, create_board_db, get_all_boards_db, get_board_by_id_db
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from src.taskflow.models.tasks import Task
from src.taskflow.schemas.contract.board_schema import BoardUpdate
from src.taskflow.schemas.contract.task_schema import TaskCreate
logger = logging.getLogger("taskflow.services.boards")

async def create_board_service(db, board_data, current_user_id: UUID):
    logger.info(
        "Creating board '%s' for user_id=%s",
        board_data.name,
        current_user_id
    )

    board = Board(
        name=board_data.name,
        description=board_data.description,
        owner_id=current_user_id
    )

    created_board = await create_board_db(db, board)

    logger.info(
        "Board created successfully with id=%s for user %s",
        created_board.id,
        current_user_id
    )

    return created_board


async def get_all_boards_service(db, current_user_id: UUID):
    logger.info(
        "Fetching all boards for user %s",
        current_user_id
    )

    boards = await get_all_boards_db(db, current_user_id)

    logger.info(f"Found {len(boards)} board(s)")

    return boards


async def get_board_by_id_service(db, board_id: UUID, current_user_id: UUID):
    logger.info(
        "Fetching board %s for user %s",
        board_id,
        current_user_id 
    )

    board = await get_board_by_id_db(db, board_id, current_user_id)

    if board is None:
        logger.warning(
            "Board %s not found",
            board_id
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )

    if board.owner_id != current_user_id:
        logger.warning(
            f"Unauthorized access. User={current_user_id}, BoardOwner={board.owner_id}"
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    logger.info(f"Board {board_id} fetched successfully")

    return board

async def update_board_service(
    db: AsyncSession,
    board_id: UUID,
    board_data: BoardUpdate,
    current_user_id: UUID,
):
    logger.info(
        "Updating board %s for user %s",
        board_id,
        current_user_id
    )

    board = await get_board_by_id_db(db, board_id, current_user_id)

    if board is None:
        logger.warning(
            "Board %s not found for user %s",
            board_id,
            current_user_id
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )

    if board.owner_id != current_user_id:
        logger.warning(
            "Unauthorized update attempt. User=%s, Owner=%s",
            current_user_id,
            board.owner_id
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    logger.debug(
        "Update data for board %s: %s",
        board_id,
        board_data.model_dump(exclude_unset=True)
    )

    updated_board = await update_board_db(db, board, board_data)

    logger.info(
        "Board %s updated successfully by user %s",
        board_id,
        current_user_id
    )

    return updated_board

async def delete_board_service(
    db: AsyncSession,
    board_id: UUID,
    current_user_id: UUID,
):
    logger.info(
        "Deleting board %s for user %s",
        board_id,
        current_user_id
    )

    board = await get_board_by_id_db(db, board_id, current_user_id)

    if board is None:
        logger.warning(
            "Board %s not found for user %s",
            board_id,
            current_user_id
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )

    if board.owner_id != current_user_id:
        logger.warning(
            "Unauthorized delete attempt. User=%s, Owner=%s",
            current_user_id,
            board.owner_id
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    deleted_board = await delete_board_db(db, board)

    logger.info(
        "Board %s deleted successfully by user %s",
        board_id,
        current_user_id
    )

    return deleted_board

async def create_task_service_board(
    db,
    board_id: UUID,
    task_data,
    current_user_id: UUID,
):
    logger.info(
        "User %s is creating a task in board %s",
        current_user_id,
        board_id
    )

    board = await get_board_by_id_db(db, board_id, current_user_id)

    if board is None:
        logger.warning(
            "Board %s not found",
            board_id
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )

    if board.owner_id != current_user_id:
        logger.warning(
            "Unauthorized access. user %s , BoardOwner= %s",
            current_user_id,
            board.owner_id
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

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
        "Task %s created successfully in board %s",
        created_task.id,
        board_id
    )

    return created_task

async def get_tasks_by_board_id_service(
    db: AsyncSession,
    board_id: UUID,
    current_user_id: UUID,
):
    logger.info(
        "User %s requested tasks for board %s",
        current_user_id,
        board_id
    )

    board = await get_board_by_id_db(db, board_id, current_user_id)

    if board is None:
        logger.warning(
            "Board %s not found for user %s",
            board_id,
            current_user_id
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )

    if board.owner_id != current_user_id:
        logger.warning(
            "Unauthorized access. User=%s, BoardOwner=%s",
            current_user_id,
            board.owner_id
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    tasks = await get_task_by_id_in_board_db(db, board_id)

    logger.info(
        "Retrieved %s task(s) from board %s",
        len(tasks),
        board_id
    )

    return tasks

async def delete_task_by_id_board_service(
    db: AsyncSession,
    board_id: UUID,
    task_id: UUID,
    current_user_id: UUID,
):
    logger.info(
        "User %s is deleting task %s from board %s",
        current_user_id,
        task_id,
        board_id
    )

    board = await get_board_by_id_db(db, board_id, current_user_id)

    if board is None:
        logger.warning(
            "Board %s not found for user %s",
            board_id,
            current_user_id
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )

    if board.owner_id != current_user_id:
        logger.warning(
            "Unauthorized delete attempt. User=%s, BoardOwner=%s",
            current_user_id,
            board.owner_id
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    task = await get_task_by_id_in_board_db(db, board_id, task_id)

    if task is None:
        logger.warning(
            "Task %s not found in board %s",
            task_id,
            board_id
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    await delete_task_db(db, task.id)

    logger.info(
        "Task %s deleted successfully from board %s",
        task_id,
        board_id
    )

    return {
        "message": "Task deleted successfully"
    }