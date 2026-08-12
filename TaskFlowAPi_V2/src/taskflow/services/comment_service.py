from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.taskflow.core.loggin import logger
from src.taskflow.crud.comment_repository import (
    create_comment_db,
    delete_comment_db,
    get_comment_by_id_db,
    update_comment_db,
)
from src.taskflow.exceptions.comment import (
    CommentCreateError,
    CommentDeleteFailed,
    CommentNotFoundError,
    CommentPermissionDenied,
    CommentUpdateError,
)

# from src.taskflow.core.loggin import setup_logging
from src.taskflow.schemas.contract.comment_schema import CommentCreate, CommentUpdate
from src.taskflow.services.board_service import get_board_by_id_service
from src.taskflow.exceptions.board import BoardNotFoundError, BoardPermissionDenied
from src.taskflow.services.task_service import get_task_by_id_service
from src.taskflow.exceptions.task import TaskNotFoundError, TaskPermissionDenied
from src.taskflow.models.comments import Comment


async def create_comment_service(
    db: AsyncSession,
    comment_create: CommentCreate,
    current_user_id: UUID,
    task_id: UUID,
    # board_id: UUID,
) -> Comment:
    logger.info(
        "create_comment_started",
        user_id=str(current_user_id),
        task_id=str(task_id),
        # board_id=str(board_id),
    )

    try:
        await get_task_by_id_service(db, task_id, current_user_id)

        new_comment = await create_comment_db(
            db, comment_create, current_user_id, task_id
        )
        logger.info(
            "create_comment_completed",
            comment_id=str(new_comment.id),
            user_id=str(current_user_id),
            task_id=str(task_id),
        )

        return new_comment
    except (CommentNotFoundError, CommentPermissionDenied, CommentCreateError):
        raise

    except Exception as e:
        logger.error(
            "create_comment_error",
            user_id=str(current_user_id),
            task_id=str(task_id),
            # board_id=str(board_id),
            error=str(e),
            exc_info=True,
        )
        raise CommentCreateError(str(e))


async def get_comment_by_id_service(
    db: AsyncSession, comment_id: UUID, current_user_id: UUID
):

    logger.info(
        "get_comment_started", comment_id=str(comment_id), user_id=str(current_user_id)
    )

    comment = await get_comment_by_id_db(db, comment_id)

    if not comment:
        logger.warning(
            "get_comment_failed",
            comment_id=str(comment_id),
            user_id=str(current_user_id),
            reason="comment_not_found",
        )
        raise CommentNotFoundError(comment_id)

    if comment.author_id != current_user_id:
        logger.warning(
            "get_comment_unauthorized",
            comment_id=str(comment_id),
            user_id=str(current_user_id),
            author_id=str(comment.author_id),
        )

        raise CommentPermissionDenied(comment.author_id)

    logger.info(
        "get_comment_success", comment_id=str(comment_id), user_id=str(current_user_id)
    )

    return comment


async def update_comment_service(
    db: AsyncSession,
    comment_id: UUID,
    update_data: CommentUpdate,
    current_user_id: UUID,
):

    logger.info(
        "update_comment_started",
        comment_id=str(comment_id),
        current_user_id=str(current_user_id),
    )

    try:
        comment = await get_comment_by_id_db(db, comment_id)

        if not comment:
            logger.warning(
                "update_comment_failed",
                comment_id=str(comment_id),
                current_user_id=str(current_user_id),
                reason="comment_not_found",
            )

            raise CommentNotFoundError(comment_id)

        if comment.author_id != current_user_id:
            logger.warning(
                "update_comment_failed",
                current_user_id=str(current_user_id),
                comment_id=str(comment_id),
                reason="unauthorized",
            )

            raise CommentPermissionDenied(comment.author_id)

        result = await update_comment_db(db, comment_id, update_data, current_user_id)

        if not result:
            logger.error(
                "update_comment_failed",
                comment_id=str(comment_id),
                error=str(e),
                exc_info=True,
                reason="db_update_failed",
            )
            raise CommentUpdateError(comment_id, "Database update operation failed")

        logger.info(
            "update_comment",
            comment_id=str(comment_id),
            current_user_id=str(current_user_id),
            reason="success",
        )

        return result

    except CommentNotFoundError:
        raise
    except CommentPermissionDenied:
        raise
    except CommentDeleteFailed:
        raise
    except CommentUpdateError:
        raise
    except Exception as e:
        logger.error(
            "update_comment_failed",
            comment_id=str(comment_id),
            error=str(e),
            exc_info=True,
            reason="db_update_failed",
        )
        raise CommentUpdateError(comment_id, "Database update operation failed")


async def delete_comment_service(
    db: AsyncSession,
    comment_id: UUID,
    current_user_id: UUID,
) -> bool:
    logger.info(
        "delete_comment_started",
        comment_id=str(comment_id),
        user_id=str(current_user_id),
    )

    try:
        comment = await get_comment_by_id_db(db, comment_id)

        if not comment:
            logger.warning(
                "delete_comment_failed",
                comment_id=str(comment_id),
                user_id=str(current_user_id),
                reason="comment_not_found",
            )
            raise CommentNotFoundError(comment_id)

        if comment.author_id != current_user_id:
            logger.warning(
                "delete_comment_failed",
                comment_id=str(comment_id),
                user_id=str(current_user_id),
                author_id=str(comment.author_id),
                reason="permission_denied",
            )
            raise CommentPermissionDenied(comment.author_id)

        result = await delete_comment_db(db, comment_id)

        if not result:
            logger.error(
                "delete_comment_failed",
                comment_id=str(comment_id),
                user_id=str(current_user_id),
                reason="db_delete_failed",
            )
            raise CommentDeleteFailed(comment_id, "Database delete operation failed")

        logger.info(
            "delete_comment_success",
            comment_id=str(comment_id),
            user_id=str(current_user_id),
        )

        return True

    except CommentNotFoundError:
        raise
    except CommentPermissionDenied:
        raise
    except CommentDeleteFailed:
        raise
    except Exception as e:
        logger.error(
            "delete_comment_error",
            comment_id=str(comment_id),
            user_id=str(current_user_id),
            error=str(e),
            exc_info=True,
        )
        raise CommentDeleteFailed(comment_id, str(e))
