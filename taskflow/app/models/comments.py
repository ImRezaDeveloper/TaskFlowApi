from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Author
    author_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # Task Comment
    task_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=True
    )

    # Board Comment
    board_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("boards.id", ondelete="CASCADE"),
        nullable=True
    )

    author = relationship(
        "User",
        back_populates="comments"
    )

    task = relationship(
        "Task",
        back_populates="comments"
    )

    board = relationship(
        "Board",
        back_populates="comments"
    )

    def __repr__(self):
        return f"<Comment {self.id}>"