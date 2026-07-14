from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from app.schemas.contract.comment_schema import CommentCreate, CommentUpdate, CommentResponse
from app.services.comment_service import (
    create_comment_service,
    get_comment_by_id_db
)
from app.db.database import get_db
from app.services.auth_service import get_current_user
router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_comment(
    task_id: UUID,
    board_id: UUID,
    comment_data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_comment_service(db, comment_data, current_user.id, task_id, board_id)


@router.get("/{comment_id}", status_code=status.HTTP_200_OK)
def get_task(
    comment_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_comment_by_id_db(db, comment_id, current_user)