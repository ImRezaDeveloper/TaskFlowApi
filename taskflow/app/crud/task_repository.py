from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from taskflow.app.models.tasks import Task
from taskflow.app.schemas.contract.task_schema import TaskCreate, TaskUpdate

async def create_task_db(db: AsyncSession, task_data: TaskCreate, user_id: UUID) -> Task:
    
    new_task = Task(
        **task_data.model_dump(),
        user_id=user_id
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

async def get_task_by_id_db(db: AsyncSession, task_id: UUID) -> Optional[Task]:
    query = select(Task).where(Task.id == task_id)
    result = await db.execute(query)
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


async def update_task_db(db: AsyncSession, task_id: UUID, update_data: TaskUpdate) -> Optional[Task]:
    task = await get_task_by_id_db(db, task_id)
    
    if not task:
        return None
    
    data_dict = update_data.model_dump(exclude_unset=True)
    
    for key, value in data_dict.items():
        setattr(task, key, value)
        
    await db.commit()
    await db.refresh(task)
    return task


async def delete_task_db(db: AsyncSession, task_id: UUID) -> bool:
    task = await get_task_by_id_db(db, task_id)
    if not task:
        return False
        
    await db.delete(task)
    await db.commit()
    return True