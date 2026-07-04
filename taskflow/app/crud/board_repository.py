from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select
from taskflow.app.models.boards import Board
from taskflow.app.schemas.contract.board_schema import BoardUpdate

def get_all_boards_db(db: AsyncSession, owner_id: UUID, current_user_id: UUID):
    stmt = select(Board).where(Board.owner_id == owner_id)

    result = db.execute(stmt)

    return result.scalars().all()

def create_board_db(db: AsyncSession, board: Board):
    db.add(board)
    db.commit()
    db.refresh(board)

    return board

def get_board_by_id_db(db: AsyncSession, board_id: UUID, current_user_id: UUID):
    stmt = select(Board).where(Board.id == board_id)

    result = db.execute(stmt)

    return result.scalar_one_or_none()

def update_board(
    db: AsyncSession,
    board: Board,
    board_data: BoardUpdate
):
    for key, value in board_data.model_dump(exclude_unset=True).items():
        setattr(board, key, value)

    db.commit()
    db.refresh(board)

    return board

def delete_board(
    db: AsyncSession,
    board: Board
):
    db.delete(board)
    db.commit()