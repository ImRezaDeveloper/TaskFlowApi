from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select
from src.taskflow.models.boards import Board
from src.taskflow.models.tasks import Task
from src.taskflow.schemas.contract.board_schema import BoardUpdate

async def get_all_boards_db(db: AsyncSession, owner_id: UUID):
    stmt = select(Board).where(Board.owner_id == owner_id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_board_db(db: AsyncSession, board: Board):
    db.add(board)
    await db.commit()          
    await db.refresh(board)    
    return board


async def get_board_by_id_db(db: AsyncSession, board_id: UUID, current_user_id: UUID):
    stmt = select(Board).where(Board.id == board_id)
    result = await db.execute(stmt)  
    return result.scalar_one_or_none()


async def update_board_db(
    db: AsyncSession,
    board: Board,
    board_data: BoardUpdate
):
    for key, value in board_data.model_dump(exclude_unset=True).items():
        setattr(board, key, value)

    await db.commit()          
    await db.refresh(board)    
    return board


async def delete_board_db(
    db: AsyncSession,
    board: Board
):
    await db.delete(board)     
    await db.commit()          


async def create_task_db(db: AsyncSession, task: Task):
    db.add(task)
    await db.commit()          
    await db.refresh(task)     
    return task


async def get_task_by_id_in_board_db(db: AsyncSession, board_id: UUID):
    stmt = select(Task).where(Task.board_id == board_id)
    result = await db.execute(stmt)  
    return result.scalars().all()


async def delete_task_by_id_in_board_db(
    db: AsyncSession,
    board_id: UUID,
    task_id: UUID,
    current_user_id: UUID
):
    stmt = select(Task).where(
        Task.id == task_id,
        Task.board_id == board_id
    )
    result = await db.execute(stmt)  
    task = result.scalar_one_or_none()

    if task is None:
        return None

    await db.delete(task)      
    await db.commit()          
    return task