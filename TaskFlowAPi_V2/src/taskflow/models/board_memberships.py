from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
import enum

from src.taskflow.db.database import Base


class Role(str, enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


class BoardMembership(Base):
    __tablename__ = "board_memberships"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    board_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("boards.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False, default=Role.MEMBER)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    board: Mapped["Board"] = relationship(
        "Board",
        back_populates="memberships"
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="board_memberships"
    )

    def __repr__(self):
        return f"<BoardMembership board_id={self.board_id} user_id={self.user_id} role={self.role}>"
