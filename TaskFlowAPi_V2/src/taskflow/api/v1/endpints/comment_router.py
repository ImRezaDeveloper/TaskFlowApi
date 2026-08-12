from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.taskflow.db.database import get_db
from src.taskflow.models.users import User
from src.taskflow.schemas.contract.comment_schema import (
    CommentCreate,
    CommentUpdate,
)
from src.taskflow.services.auth_service import get_current_user
from src.taskflow.services.comment_service import (
    create_comment_service,
    delete_comment_service,
    get_comment_by_id_service,
    update_comment_service,
)

router = APIRouter(prefix="/tasks/{task_id}/comments", tags=["Comments"])


@router.post(
    "/boards/{board_id}/tasks/{task_id}/comments/", status_code=status.HTTP_201_CREATED
)
async def create_comment(
    task_id: UUID,
    board_id: UUID,
    comment_data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_comment_service(
        db, comment_data, current_user.id, task_id, board_id
    )


@router.get("/{comment_id}", status_code=status.HTTP_200_OK)
async def get_comment(
    comment_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_comment_by_id_service(db, comment_id, current_user.id)


@router.patch("/{comment_id}", status_code=status.HTTP_200_OK)
async def update_comment(
    comment_id: UUID,
    comment_data: CommentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await update_comment_service(db, comment_id, comment_data, current_user.id)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await delete_comment_service(db, comment_id, current_user.id)
