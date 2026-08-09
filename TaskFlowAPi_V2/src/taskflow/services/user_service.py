from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.taskflow.core.loggin import logger
from src.taskflow.crud.user_repository import (
    create_user_db,
    delete_user_db,
    get_user_by_email,
    get_user_by_name,
    get_users_db,
    update_user_db,
    verify_exists_user,
)
from src.taskflow.crud.user_repository import get_user_by_id as get_user_id
from src.taskflow.exceptions.user import (
    EmailAlreadyExistError,
    UserAlreadyExistError,
    UserCreationError,
    UserDeleteError,
    UserNotFoundError,
)
from src.taskflow.models.users import User
from src.taskflow.schemas.contract.user_schema import UserUpdate


def get_users(db: AsyncSession):
    users = get_users_db(db)
    return users


async def get_user_by_id(user_id: UUID, db: AsyncSession, current_user_id) -> User:
    logger.info("get_user_by_id_started", user_id=str(user_id))

    existing_user = await get_user_id(db, user_id)

    if not existing_user:
        logger.warning("get_user_by_id_failed", reason="user_not_found")
        raise UserNotFoundError(user_id)

    logger.info("get_user_by_id", user_id=str(user_id), status="success")

    return existing_user


async def create_user(
    username: str,
    email: str,
    hashed_password: str,
    full_name: str,
    is_active: bool,
    is_verified: bool,
    db: AsyncSession,
):
    logger.info(
        "create_user_started",
        username=username,
        email=email,
        full_name=full_name,
        is_active=is_active,
        is_verified=is_verified,
    )

    try:
        existing_email = await verify_exists_user(db, email)
        if existing_email:
            logger.warning(
                "create_user_failed",
                username=username,
                email=email,
                reason="email_already_exists",
            )
            raise EmailAlreadyExistError("email", email)

        existing_username = await get_user_by_name(db, username)
        if existing_username:
            logger.warning(
                "create_user_failed",
                username=username,
                email=email,
                reason="username_already_exists",
            )
            raise UserAlreadyExistError("username", username)

        new_user = await create_user_db(
            username, email, hashed_password, full_name, is_active, is_verified, db
        )

        # Transaction
        await db.commit()
        await db.refresh(new_user)

        logger.info(
            "create_user_success",
            user_id=str(new_user.id),
            username=username,
            email=email,
        )

        return new_user

    except UserAlreadyExistError:
        raise

    except Exception as e:
        await db.rollback()
        logger.error(
            "create_user_error",
            username=username,
            email=email,
            error=str(e),
            exc_info=True,
        )
        raise UserCreationError(username, email, str(e))


from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.taskflow.exceptions.user import UserNotFoundError, UserUpdateError


async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: AsyncSession,
):
    logger.info(
        "update_user_started",
        user_id=str(user_id),
        update_fields=list(user_data.model_dump(exclude_unset=True).keys()),
    )

    try:
        user = await get_user_by_id(db, user_id)

        if not user:
            logger.warning(
                "update_user_failed", user_id=str(user_id), reason="user_not_found"
            )
            raise UserNotFoundError(user_id)

        if user_data.email and user_data.email != user.email:
            existing_user = await get_user_by_email(db, user_data.email)
            if existing_user:
                logger.warning(
                    "update_user_failed",
                    user_id=str(user_id),
                    email=user_data.email,
                    reason="email_already_exists",
                )
                raise EmailAlreadyExistError("email", user_data.email)

        if user_data.username and user_data.username != user.username:
            existing_user = await get_user_by_name(db, user_data.username)
            if existing_user:
                logger.warning(
                    "update_user_failed",
                    user_id=str(user_id),
                    username=user_data.username,
                    reason="username_already_exists",
                )
                raise UserAlreadyExistError("username", user_data.username)

        updated_user = await update_user_db(db, user, user_data)

        await db.commit()
        await db.refresh(updated_user)

        logger.info(
            "update_user_success",
            user_id=str(user_id),
            updated_fields=list(user_data.model_dump(exclude_unset=True).keys()),
        )

        return updated_user

    except (UserNotFoundError, UserAlreadyExistError):
        raise

    except Exception as e:
        await db.rollback()
        logger.error(
            "update_user_error",
            user_id=str(user_id),
            error=str(e),
            exc_info=True,
        )
        raise UserUpdateError(user_id, str(e))


async def delete_user(
    user_id: UUID,
    db: AsyncSession,
):
    logger.info("delete_user_started", user_id=str(user_id))
    try:
        user = await get_user_by_id(user_id, db)

        if not user:
            logger.warning(
                "delete_user_failed", user_id=str(user_id), reason="user_not_found"
            )
            raise UserNotFoundError(user_id)

        await delete_user_db(db, user_id)

        await db.commit()

        logger.info("delete_user_success", user_id=str(user_id))

        return {"message": "User deleted successfully"}
    except (UserNotFoundError):
        raise
    except Exception as e:
        await db.rollback()
        logger.error(
            "delete_user_error",
            user_id=str(user_id),
            error=str(e),
            exc_info=True,
        )
        raise UserDeleteError(user_id, str(e))