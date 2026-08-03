from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.taskflow.db.database import get_db
from src.taskflow.models.users import User
from src.taskflow.schemas.contract.board_schema import (
    BoardCreate,
    BoardUpdate,
)
from src.taskflow.schemas.contract.task_schema import TaskCreate, TaskResponse
from src.taskflow.services.auth_service import get_current_user
from src.taskflow.services.board_service import (
    create_board_service,
    create_task_service_board,
    delete_board_service,
    delete_task_by_id_board_service,
    get_all_boards_service,
    get_board_by_id_service,
    get_tasks_by_board_id_service,
    update_board_service,
)

router = APIRouter(prefix="/boards", tags=["Boards"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_board(
    board_data: BoardCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_board_service(db, board_data, current_user.id)


@router.get("/{board_id}", status_code=status.HTTP_200_OK)
async def get_board(
    board_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_board_by_id_service(db, board_id, current_user.id)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_boards(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return await get_all_boards_service(db, current_user.id)


@router.put("/{board_id}", response_model=BoardUpdate, status_code=status.HTTP_200_OK)
async def update_board(
    board_id: UUID,
    board_data: BoardUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await update_board_service(db, board_id, board_data, current_user.id)


@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_board(
    board_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await delete_board_service(db, board_id, current_user.id)


# board_tasks
@router.post(
    "/{board_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task_in_board(
    board_id: UUID,
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_task_service_board(
        db=db,
        board_id=board_id,
        task_data=task_data,
        current_user_id=current_user.id,
    )


@router.get(
    "/{board_id}/tasks",
    response_model=list[TaskResponse],
    status_code=status.HTTP_200_OK,
)
async def get_tasks_in_board(
    board_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_tasks_by_board_id_service(db, board_id, current_user.id)


@router.delete("/{board_id}/task", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_in_board(
    board_id: UUID,
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await delete_task_by_id_board_service(db, board_id, task_id, current_user.id)
