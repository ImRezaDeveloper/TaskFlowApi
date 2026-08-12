from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.taskflow.db.database import get_db
from src.taskflow.models.users import User
from src.taskflow.schemas.contract.task_schema import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from src.taskflow.services.auth_service import get_current_user
from src.taskflow.services.task_service import (
    create_task_service,
    delete_task_service,
    get_board_tasks_service,
    get_task_by_id_service,
    update_task_service,
)
from src.taskflow.schemas.contract.comment_schema import CommentCreate
from src.taskflow.services.comment_service import create_comment_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_task_service(db, task_data, current_user.id)


@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def get_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_task_by_id_service(db, task_id, current_user.id)


@router.put("/{task_id}", status_code=status.HTTP_200_OK)
async def update_task(
    task_id: UUID,
    update_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await update_task_service(db, task_id, update_data, current_user.id)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await delete_task_service(db, task_id, current_user.id)


@router.post("/{task_id}/comments/", status_code=status.HTTP_201_CREATED)
async def create_comment(
    task_id: UUID,
    # board_id: UUID,
    comment_data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_comment_service(db, comment_data, current_user.id, task_id)
