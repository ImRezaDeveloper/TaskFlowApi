import logging
import time
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.taskflow.models.tasks import Task
from src.taskflow.schemas.contract.task_schema import TaskCreate, TaskUpdate

logger = logging.getLogger("taskflow.repository.tasks")


async def create_task_db(
    db: AsyncSession, task_data: TaskCreate, user_id: UUID
) -> Task:
    new_task = Task(**task_data.model_dump(), user_id=user_id)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


async def get_task_by_id_db(db: AsyncSession, task_id: UUID) -> Task | None:
    query = select(Task).where(Task.id == task_id)
    result = await db.execute(query)
    return result.scalars().first()


async def get_board_tasks_db(
    db: AsyncSession, board_id: UUID, skip: int = 0, limit: int = 100
) -> list[Task]:
    start = time.perf_counter()

    query = select(Task).where(Task.board_id == board_id).offset(skip).limit(limit)
    result = await db.execute(query)
    print(f"{time.perf_counter() - start:.6f} sec")
    return list(result.scalars().all())


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


async def delete_task_db(db: AsyncSession, task_id: UUID) -> bool:
    task = await get_task_by_id_db(db, task_id)
    if not task:
        return False

    await db.delete(task)
    await db.commit()

    check_stmt = select(Task).where(Task.id == task_id)
    check_result = await db.execute(check_stmt)
    check_test = check_result.scalars().first()
    logger.info(f"🔍 After commit, task exists? {check_test is not None}")

    return True
