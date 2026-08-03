from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.taskflow.schemas.contract.task_schema import TaskResponse


class BoardBase(BaseModel):
    name: str
    description: str | None = None


class BoardCreate(BoardBase):
    name: str
    description: str | None = None


class BoardUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class BoardResponse(BoardBase):
    id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    tasks: list[TaskResponse] = []

    model_config = ConfigDict(from_attributes=True)
