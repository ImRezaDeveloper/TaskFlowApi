from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from app.crud.task_repository import delete_task_db
from app.models.boards import Board
from app.crud.board_repository import create_task_db, delete_task_by_id_in_board_db, get_task_by_id_in_board_db, update_board_db, delete_board_db, create_board_db, get_all_boards_db, get_board_by_id_db
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.models.tasks import Task
from app.schemas.contract.board_schema import BoardUpdate
from app.schemas.contract.task_schema import TaskCreate
logger = logging.getLogger("taskflow.services.boards")


def create_board_service(db, board_data, current_user_id: UUID):
    logger.info(f"Creating board '{board_data.name}' for user {current_user_id}")

    board = Board(
        name=board_data.name,
        description=board_data.description,
        owner_id=current_user_id
    )

    created_board = create_board_db(db, board)

    logger.info(f"Board created successfully with id={created_board.id}")

    return created_board


def get_all_boards_service(db, current_user_id: UUID):
    logger.info(f"Fetching all boards for user {current_user_id}")

    boards = get_all_boards_db(db, current_user_id)

    logger.info(f"Found {len(boards)} board(s)")

    return boards


def get_board_by_id_service(db, board_id: UUID, current_user_id: UUID):
    logger.info(f"Fetching board {board_id} for user {current_user_id}")

    board = get_board_by_id_db(db, board_id)

    if board is None:
        logger.warning(f"Board {board_id} not found")

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

def update_board_service(
    db,
    board_id: UUID,
    board_data: BoardUpdate,
    current_user_id: UUID,
):
    logger.info(f"Updating board {board_id} for user {current_user_id}")

    board = get_board_by_id_db(db, board_id, current_user_id)

    if board is None:
        logger.warning(f"Board {board_id} not found")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )

    if board.owner_id != current_user_id:
        logger.warning(
            f"Unauthorized update attempt. User={current_user_id}, Owner={board.owner_id}"
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    updated_board = update_board_db(db, board, board_data)

    logger.info(f"Board {board_id} updated successfully")

    return updated_board

def delete_board_service(db, board_id: UUID, current_user_id: UUID):
    
    logger.info(f"Deleting board {board_id} for user {current_user_id}")

    board = get_board_by_id_db(db, board_id)

    if board is None:
        logger.warning(f"Board {board_id} not found")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )

    if board.owner_id != current_user_id:
        logger.warning(
            f"Unauthorized update attempt. User={current_user_id}, Owner={board.owner_id}"
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    delete_board = delete_board_db(db, board)

    logger.info(f"Board {board_id} deleted successfully")

    return delete_board

def create_task_service_board(
    db,
    board_id: UUID,
    task_data,
    current_user_id: UUID,
):
    logger.info(
        f"User {current_user_id} is creating a task in board {board_id}"
    )

    board = get_board_by_id_db(db, board_id, current_user_id)

    if board is None:
        logger.warning(f"Board {board_id} not found")

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

    task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        due_date=task_data.due_date,
        user_id=current_user_id,
        board_id=board.id,
    )

    created_task = create_task_db(db, task)

    logger.info(
        f"Task {created_task.id} created successfully in board {board.id}"
    )

    return created_task

def get_tasks_by_board_id_service(
    db,
    board_id: UUID,
    current_user_id: UUID,
):
    logger.info(
        f"User {current_user_id} requested tasks for board {board_id}"
    )

    board = get_board_by_id_db(db, board_id, current_user_id)

    if board is None:
        logger.warning(f"Board {board_id} not found")

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

    tasks = get_task_by_id_in_board_db(db, board_id)

    logger.info(
        f"Retrieved {len(tasks)} task(s) from board {board_id}"
    )

    return tasks

def delete_task_by_id_board_service(
    db,
    board_id: UUID,
    task_id: UUID,
    current_user_id: UUID,
):
    logger.info(
        f"User {current_user_id} is deleting task {task_id} from board {board_id}"
    )

    board = get_board_by_id_db(db, board_id, current_user_id)

    if board is None:
        logger.warning(f"Board {board_id} not found")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )

    if board.owner_id != current_user_id:
        logger.warning(
            f"Unauthorized delete attempt. User={current_user_id}, BoardOwner={board.owner_id}"
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    task = get_task_by_id_in_board_db(db, board_id, task_id)

    if task is None:
        logger.warning(
            f"Task {task_id} not found in board {board_id}"
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task = get_task_by_id_in_board_db(db, board_id, task_id)

    if task is None:
        raise HTTPException(...)

    delete_task_db(db, task.id)

    logger.info(
        f"Task {task_id} deleted successfully from board {board_id}"
    )

    return {
        "message": "Task deleted successfully"
    }