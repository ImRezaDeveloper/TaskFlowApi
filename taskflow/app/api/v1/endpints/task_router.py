from typing import List
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from taskflow.app.db.database import get_db
from taskflow.app.schemas.contract.task_schema import TaskCreate, TaskBase
from taskflow.app.services.user_service import get_user_by_id as get_user_id
from taskflow.app.services.user_service import create_user, hash_pwd
# from taskflow.app.services.task_service import get_board_tasks_service, delete_user, get, create_user
from taskflow.app.services.auth_service import get_current_user
from taskflow.app.security.auth.auth_dependencies import require_admin

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.get("/", status_code=status.HTTP_200_OK)
def create_task(db: AsyncSession = Depends(get_db)):
    return {"admin"}