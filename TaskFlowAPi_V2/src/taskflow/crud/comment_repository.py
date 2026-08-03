from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.taskflow.crud.task_repository import get_task_by_id_db
from src.taskflow.models.comments import Comment
from src.taskflow.models.tasks import Task
from src.taskflow.schemas.contract.comment_schema import CommentCreate, CommentUpdate
from src.taskflow.schemas.contract.task_schema import TaskUpdate


async def create_comment_db(
    db: AsyncSession,
    comment_data: CommentCreate,
    author_id: UUID | None = None,
    task_id: UUID | None = None,
    board_id: UUID | None = None,
) -> Comment:
    new_comment = Comment(
        **comment_data.model_dump(),
        author_id=author_id,
        task_id=task_id,
        board_id=board_id,
    )

    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)

    return new_comment


async def get_comment_by_id_db(db: AsyncSession, comment_id: UUID) -> Comment | None:
    query = select(Comment).where(Comment.id == comment_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_comments_by_task_id_db(
    db: AsyncSession, task_id: UUID, skip: int = 0, limit: int = 100
) -> list[Comment]:
    query = select(Comment).where(Comment.task_id == task_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def update_comment_db(
    db: AsyncSession,
    comment_id: UUID,
    update_data: CommentUpdate,
    current_user_id: UUID,
) -> Comment | None:
    comment = await get_comment_by_id_db(db, comment_id)

    if not comment:
        return None

    data_dict = update_data.model_dump(exclude_unset=True)

    for key, value in data_dict.items():
        setattr(comment, key, value)

    await db.commit()
    await db.refresh(comment)
    return comment


async def delete_comment_db(db: AsyncSession, comment_id: UUID) -> bool:
    comment = await get_comment_by_id_db(db, comment_id)
    if not comment:
        return False

    await db.delete(comment)
    await db.commit()
    return True


async def update_task_db(
    db: AsyncSession, task_id: UUID, update_data: TaskUpdate
) -> Task | None:
    task = await get_task_by_id_db(db, task_id)

    if not task:
        return None

    data_dict = update_data.model_dump(exclude_unset=True)

    for key, value in data_dict.items():
        setattr(task, key, value)

    await db.commit()
    await db.refresh(task)
    return task
