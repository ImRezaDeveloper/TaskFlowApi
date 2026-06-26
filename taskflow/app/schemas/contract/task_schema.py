from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from taskflow.app.models.tasks import TaskStatus, TaskPriority # ایمپورت Enumهایی که توی مدل ساختیم

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="عنوان تسک")
    description: Optional[str] = Field(None, description="توضیحات تکمیلی تسک")
    status: TaskStatus = Field(default=TaskStatus.TODO)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: Optional[datetime] = Field(None, description="تاریخ ددلاین تسک")

class TaskCreate(TaskBase):
    title: str = Field(..., min_length=1, max_length=100, description="عنوان تسک")
    description: Optional[str] = Field(None, description="توضیحات تکمیلی تسک")
    status: TaskStatus = Field(default=TaskStatus.TODO)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: Optional[datetime] = Field(None, description="تاریخ ددلاین تسک")
    board_id: UUID = Field(..., description="آیدی بوردی که تسک متعلق به آن است")

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    board_id: Optional[UUID] = None

class TaskResponse(TaskBase):
    id: UUID
    board_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
