import logging
from uuid import UUID
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.loggin import setup_logging
from app.models.users import User
from app.schemas.contract.comment_schema import CommentCreate

setup_logging()
logger = logging.getLogger(__name__)

from app.crud.comment_repository import (
    create_comment_db,
    get_comment_by_id_db,
    get_comments_by_task_id_db,
    update_comment_db,
    delete_comment_db
)
# from taskflow.app.schemas.contract.comment_schema import CommentCreate, CommentUpdate
# from taskflow.app.models.comments import Comment


def create_comment_service(db: AsyncSession, comment_create: CommentCreate, current_user_id: UUID, task_id: UUID, board_id: UUID):

    try:
        new_comment = create_comment_db(db, comment_create, current_user_id, task_id, board_id)
        logger.info(f"Comment successfully created with ID {new_comment.id} by user {current_user_id}")
    except Exception as e:
        logger.error(f"Failed to create comment for user {current_user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="there was an error in creating comment"
        )
        
    return new_comment
        
def get_task_by_id_service(db, comment_id: UUID, current_user_id: UUID):
    logger.info(f"User {current_user_id} requested comment ID {comment_id}")
    
    comment = get_comment_by_id_db(db, comment_id)
    
    if not comment:
        logger.warning(f"Comment ID {comment_id} not found in database.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="your current comment not found!"
        )
        
    if comment.author_id != current_user_id:
        logger.warning(f"Unauthorized access attempt! User {current_user_id} tried to view comment {comment_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you don't have permission to do this!"
        )
        
    return comment