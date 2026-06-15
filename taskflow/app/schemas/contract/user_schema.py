from enum import Enum
from pydantic import EmailStr, BaseModel
from pydantic import BaseModel, EmailStr
from typing import Optional

class RoleEnum(str, Enum):
    ADMIN = "1"
    USER = "2"
    MANAGER = "3"

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    roles: RoleEnum


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserDisplay(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True