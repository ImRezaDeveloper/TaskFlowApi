from enum import Enum
from pydantic import EmailStr, BaseModel
from pydantic import BaseModel, EmailStr
from typing import Optional

class RoleEnum(str, Enum):
    ADMIN = "1"
    USER = "2"
    MEMBERSHIP = "3"

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    full_name: str
    is_active: bool
    is_verified: bool

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserDisplay(BaseModel):
    # id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True