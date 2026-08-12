from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.taskflow.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    full_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )
    boards: Mapped[list["Board"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )
    board_memberships: Mapped[list["BoardMembership"]] = relationship(
        "BoardMembership",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    

    # def __repr__(self) -> str:
    #     return f"<User {self.username}>"
