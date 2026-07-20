from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tasks import Task
from app.schemas.contract.task_schema import TaskCreate, TaskUpdate
import logging

logger = logging.getLogger("taskflow.repository.tasks")

def create_task_db(db: AsyncSession, task_data: TaskCreate, user_id: UUID) -> Task:
    
    new_task = Task(
        **task_data.model_dump(),
        user_id=user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_task_by_id_db(db: AsyncSession, task_id: UUID) -> Optional[Task]:
    query = select(Task).where(Task.id == task_id)
    result = db.execute(query)
    return result.scalars().first()


async def get_board_tasks_db(db: AsyncSession, board_id: UUID, skip: int = 0, limit: int = 100) -> List[Task]:
    query = (
        select(Task)
        .where(Task.board_id == board_id)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
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


async def delete_task_db(db: AsyncSession, task_id: UUID) -> bool:
    task = get_task_by_id_db(db, task_id)
    if not task:
        return False
        
    await db.delete(task)   # ← Add await
    await db.commit()       # ← Add await
    check_test = db.get(db, task_id)
    logger.info(f"🔍 After commit, task exists? {check_test is not None}")
    return True