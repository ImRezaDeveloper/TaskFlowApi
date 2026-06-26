from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from taskflow.app.db.database import Base
class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus), 
        default=TaskStatus.TODO, 
        nullable=False
    )
    priority: Mapped[TaskPriority] = mapped_column(
        SQLEnum(TaskPriority), 
        default=TaskPriority.MEDIUM, 
        nullable=False
    )

    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow, 
        nullable=False
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    owner: Mapped["User"] = relationship(back_populates="tasks")

    def __repr__(self) -> str:
        return f"<Task {self.title} - {self.status}>"