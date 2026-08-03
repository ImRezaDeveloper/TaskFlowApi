from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.taskflow.models.users import User
from src.taskflow.schemas.contract.user_schema import UserUpdate


async def get_users_db(db: AsyncSession) -> list[User]:
    query = select(User)
    result = await db.execute(query)
    return list(result.scalars().all())


async def verify_exists_user(db: AsyncSession, email: str) -> bool:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none() is not None


async def create_user_db(
    username: str,
    email: str,
    hashed_password: str,
    full_name: str,
    is_active: bool,
    is_verified: bool,
    db: AsyncSession,
) -> User:
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        is_active=is_active,
        is_verified=is_verified,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def get_user_by_id(db: AsyncSession, user_id: UUID) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_name(db: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def update_user_db(
    db: AsyncSession,
    user: User,
    user_data: UserUpdate,
) -> User:
    for key, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)

    return user


async def delete_user_db(db: AsyncSession, user_id: UUID) -> User | None:
    user = await get_user_by_id(db, user_id)

    if user is None:
        return None

    await db.delete(user)
    await db.commit()

    return user


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
