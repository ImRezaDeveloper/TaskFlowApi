from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from app.db.database import get_db
from app.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.contract.user_schema import UserUpdate

def get_users_db(db: AsyncSession):
    query = select(User)
    result = db.execute(query)
    tasks = result.scalars().all()
    
    return tasks

def verify_exists_user(db: AsyncSession, email: str) -> bool:
    stmt = select(User).where(User.email == email)

    result = db.execute(stmt)

    return result.scalar_one_or_none() is not None

def create_user_db(username, email, hashed_password, full_name, is_active, is_verified, get_db: AsyncSession = Depends(get_db)):

    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        is_active=is_active,
        is_verified=is_verified
    )
    
    get_db.add(new_user)
    get_db.commit()
    get_db.refresh(new_user)
    
    return new_user

def get_user_by_id(db: AsyncSession, user_id: UUID):
    stmt = select(User).where(User.id == user_id)

    result = db.execute(stmt)
    return result.scalar_one_or_none()

def update_user_db(
    user_data: UserUpdate,
    user: User,
    db: AsyncSession,
):
    for key, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user

def delete_user_db(db: AsyncSession, user_id: UUID):
    user = get_user_by_id(db, user_id)

    if user is None:
        return None

    db.delete(user)
    db.commit()

    return user

def get_user_by_email(db: AsyncSession, email: str):
    stmt = select(User).where(User.email == email)

    result = db.execute(stmt)

    return result.scalar_one_or_none()
