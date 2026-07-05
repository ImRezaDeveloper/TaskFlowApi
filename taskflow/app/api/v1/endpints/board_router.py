from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from taskflow.app.models.boards import Board
from taskflow.app.models.users import User
from taskflow.app.schemas.contract.board_schema import BoardCreate, BoardUpdate, BoardResponse
from taskflow.app.schemas.contract.task_schema import TaskCreate, TaskResponse
from taskflow.app.services.board_service import (
    create_board_service,
    create_task_service_board,
    get_all_boards_service,
    get_board_by_id_service,
    update_board_service,
    delete_board_service,
    get_tasks_by_board_id_service,
    delete_task_by_id_in_board_db
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

@router.get("/", response_model=list[BoardResponse], status_code=status.HTTP_200_OK)
def get_all_boards(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_boards_service(
        db,
        current_user.id
    )

@router.put(
    "/{board_id}",
    response_model=BoardUpdate,
    status_code=status.HTTP_200_OK
)
def update_board(
    board_id: UUID,
    board_data: BoardUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_board_service(
        db,
        board_id,
        board_data,
        current_user.id
    )
    
@router.delete('/{board_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_board(
    board_id: UUID, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return delete_board_service(db, board_id, current_user)

# board_tasks

@router.post(
    "/{board_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task_in_board(
    board_id: UUID,
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_task_service_board(
        db=db,
        board_id=board_id,
        task_data=task_data,
        current_user_id=current_user.id,
    )
    
@router.get('/{board_id}/tasks', response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
def get_tasks_in_board(
    board_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user_id: User = Depends(get_current_user)
):
    
    return get_tasks_by_board_id_service(db, board_id, current_user_id)

@router.delete('/{board_id}/task', status_code=status.HTTP_204_NO_CONTENT)
def get_tasks_in_board(
    board_id: UUID,
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user_id: User = Depends(get_current_user)
):
    
    return delete_task_by_id_in_board_db(db, board_id, task_id, current_user_id)