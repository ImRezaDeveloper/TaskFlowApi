from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.taskflow.models.tasks import TaskPriority, TaskStatus
from src.taskflow.schemas.contract.comment_schema import (
    CommentResponse,  # ایمپورت Enumهایی که توی مدل ساختیم
)


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="عنوان تسک")
    description: str | None = Field(None, description="توضیحات تکمیلی تسک")
    status: TaskStatus = Field(default=TaskStatus.TODO)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: datetime | None = Field(None, description="تاریخ ددلاین تسک")


class TaskCreate(TaskBase):
    title: str = Field(..., min_length=1, max_length=100, description="عنوان تسک")
    description: str | None = Field(None, description="توضیحات تکمیلی تسک")
    status: TaskStatus = Field(default=TaskStatus.TODO)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: datetime | None = Field(None, description="تاریخ ددلاین تسک")
    board_id: UUID = Field(..., description="آیدی بوردی که تسک متعلق به آن است")


class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None
    # board_id: Optional[UUID] = None


class TaskResponse(TaskBase):
    id: UUID
    # board_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    comments: list[CommentResponse] = []

    model_config = ConfigDict(from_attributes=True)
