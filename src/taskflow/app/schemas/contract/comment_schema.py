from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class CommentBase(BaseModel):
    content: str
    

class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    content: str


class CommentResponse(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    author_id: UUID

    task_id: UUID | None = None
    board_id: UUID | None = None

    created_at: datetime
    updated_at: datetime