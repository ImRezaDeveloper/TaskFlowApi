from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.db.database import Base

# کلاس پایه برای مدل‌ها

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    full_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    # avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False) # برای تایید ایمیل
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow, 
        nullable=False
    )

    """
    tasks: Mapped[List["Task"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
    boards: Mapped[List["Board"]] = relationship(back_populates="creator", cascade="all, delete-orphan")
    """

    def __repr__(self) -> str:
        return f"<User {self.username}>"