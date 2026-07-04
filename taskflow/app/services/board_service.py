from uuid import UUID

from fastapi import HTTPException, status
from taskflow.app.models.boards import Board
from taskflow.app.crud.board_repository import create_board_db, get_all_boards_db, get_board_by_id_db
from sqlalchemy.ext.asyncio import AsyncSession
import logging
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