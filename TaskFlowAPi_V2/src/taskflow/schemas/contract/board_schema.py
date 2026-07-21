from uuid import UUID
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from src.taskflow.schemas.contract.task_schema import TaskResponse


class BoardBase(BaseModel):
    name: str
    description: Optional[str] = None
    

class BoardCreate(BoardBase):
    name: str
    description: Optional[str] = None


class BoardUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class BoardResponse(BoardBase):
    id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: datetime
    
    tasks: list[TaskResponse] = []

    model_config = ConfigDict(from_attributes=True)