from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    full_name: str | None = None
    is_active: bool
    is_verfied: bool


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserResponse(UserBase):
    id: UUID
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)