from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from taskflow.app.models.boards import Board
from taskflow.app.models.users import User
from taskflow.app.schemas.contract.board_schema import BoardCreate, BoardUpdate, BoardResponse
from taskflow.app.services.board_service import (
    create_board_service,
    get_all_boards_service,
    get_board_by_id_service
)

from taskflow.app.db.database import get_db
from taskflow.app.services.auth_service import get_current_user
router = APIRouter(prefix="/boards", tags=["Boards"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_board(
    task_data: BoardCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_board_service(db, task_data, current_user.id)


@router.get("/{task_id}", status_code=status.HTTP_200_OK)
def get_task(
    board_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_board_by_id_service(db, board_id, current_user.id)

