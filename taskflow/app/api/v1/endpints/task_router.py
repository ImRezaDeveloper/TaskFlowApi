from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from taskflow.app.schemas.contract.task_schema import TaskCreate, TaskUpdate, TaskResponse
from taskflow.app.services.task_service import (
    create_task_service,
    get_task_by_id_service,
    get_board_tasks_service,
    update_task_service,
    delete_task_service
)
from taskflow.app.db.database import get_db
from taskflow.app.services.auth_service import get_current_user
router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await create_task_service(db, task_data, current_user.id)


@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def get_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await get_task_by_id_service(db, task_id, current_user.id)


@router.get("/board/{board_id}", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
async def get_board_tasks(
    board_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await get_board_tasks_service(db, board_id, current_user.id, skip, limit)


@router.patch("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def update_task(
    task_id: UUID,
    update_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await update_task_service(db, task_id, update_data, current_user.id)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    await delete_task_service(db, task_id, current_user.id)
    return None