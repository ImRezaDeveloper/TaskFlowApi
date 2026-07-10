from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from taskflow.app.crud.task_repository import get_task_by_id_db
from taskflow.app.models.comments import Comment
from taskflow.app.models.tasks import Task
from taskflow.app.schemas.contract.comment_schema import CommentCreate, CommentUpdate
from taskflow.app.schemas.contract.task_schema import TaskUpdate

def create_comment_db(
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
    db.commit()
    db.refresh(new_comment)

    return new_comment

def get_comment_by_id_db(db: AsyncSession, comment_id: UUID, current_user_id: UUID) -> Optional[Comment]:
    query = select(Comment).where(Comment.id == comment_id)
    result = db.execute(query)
    return result.scalar_one_or_none()


def get_comments_by_task_id_db(db: AsyncSession, task_id: UUID, skip: int = 0, limit: int = 100) -> List[Comment]:
    query = (
        select(Comment)
        .where(Comment.task_id == task_id)
        .offset(skip)
        .limit(limit)
    )
    result = db.execute(query)
    return list(result.scalars().all())


def update_task_db(db: AsyncSession, task_id: UUID, update_data: TaskUpdate) -> Optional[Task]:
    task = get_task_by_id_db(db, task_id)
    
    if not task:
        return None
    
    data_dict = update_data.model_dump(exclude_unset=True)
    
    for key, value in data_dict.items():
        setattr(task, key, value)
        
    db.commit()
    db.refresh(task)
    return task
def update_comment_db(db: AsyncSession, comment_id: UUID, update_data: CommentUpdate) -> Optional[Comment]:
    comment = get_comment_by_id_db(db, comment_id)
    
    if not comment:
        return None
    
    data_dict = update_data.model_dump(exclude_unset=True)
    
    for key, value in data_dict.items():
        setattr(comment, key, value)
        
    db.commit()
    db.refresh(comment)
    return comment

def delete_comment_db(db: AsyncSession, comment_id: UUID) -> bool:
    comment = get_comment_by_id_db(db, comment_id)
    
    if not comment:
        return False
        
    db.delete(comment)
    db.commit()
    return True