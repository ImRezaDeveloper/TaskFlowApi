from src.taskflow.core.loggin import logger
from uuid import UUID
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
# from src.taskflow.core.loggin import setup_logging
from src.taskflow.models.users import User
from src.taskflow.schemas.contract.comment_schema import CommentCreate, CommentUpdate
from src.taskflow.crud.comment_repository import (
    create_comment_db,
    get_comment_by_id_db,
    get_comments_by_task_id_db,
    update_comment_db,
    delete_comment_db
)


async def create_comment_service(  
    db: AsyncSession,
    comment_create: CommentCreate,
    current_user_id: UUID,
    task_id: UUID,
    board_id: UUID,
):
    logger.info(
        "create_comment_started",
        user_id=str(current_user_id),
        task_id=str(task_id),
        board_id=str(board_id)
    )

    try:
        new_comment = await create_comment_db(  
            db, comment_create, current_user_id, task_id, board_id
        )
        logger.info(
            "create_comment_completed",
            comment_id=str(new_comment.id),
            user_id=str(current_user_id),
            task_id=str(task_id)
        )

        return new_comment
    except Exception as e:
        logger.error(
            "create_comment_failed",
            user_id=str(current_user_id),
            task_id=str(task_id),
            error= str(e),
            exc_info=True
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="there was an error in creating comment"
        )
        
async def get_comment_by_id_service(db: AsyncSession, comment_id: UUID,current_user_id: UUID):

    logger.info(
        "get_comment_started",
        comment_id=str(comment_id),
        user_id=str(current_user_id)
    )
    
    comment = await get_comment_by_id_db(db, comment_id)  

    
    if not comment:
        logger.warning(
            "get_comment_failed",
            comment_id=str(comment_id),
            user_id=str(current_user_id),
            reason="comment_not_found"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="your current comment not found!"
        )
        
    if comment.author_id != current_user_id:
        logger.warning(
            "get_comment_unauthorized",
            comment_id=str(comment_id),
            user_id=str(current_user_id),
            author_id=str(comment.author_id)
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you don't have permission to do this!"
        )

    logger.info(
        "get_comment_success",
        comment_id=str(comment_id),
        user_id=str(current_user_id)
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
        current_user_id=str(current_user_id)
    )

    try:
        comment = await update_comment_db(  
            db, comment_id, update_data, current_user_id
        )
        
        if not comment:
            logger.warning(
                "update_comment_failed",
                comment_id=str(comment_id),
                current_user_id=str(current_user_id),
                reason="comment_not_found"
            )

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )
        
        if comment.author_id != current_user_id:
            logger.warning(
                "update_comment_failed",
                current_user_id=str(current_user_id),
                comment_id=str(comment_id),
                reason="unauthorized"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to update this comment"
            )
        
        logger.info(f"Comment {comment_id} successfully updated by user {current_user_id}")
        logger.info(
            "update_comment",
            comment_id=str(comment_id),
            current_user_id=str(current_user_id),
            reason="success"
        )

        return comment
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "update_comment_failed",
            comment_id=str(comment_id),
            error=str(e),
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="There was an error updating the comment"
        )

async def delete_comment_service(  
    db: AsyncSession, 
    comment_id: UUID, 
    current_user_id: UUID
) -> bool:
    try:
        comment = await get_comment_by_id_db(db, comment_id)  
        
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        
        if comment.author_id != current_user_id:
            raise HTTPException(status_code=403, detail="Permission denied")
        
        result = await delete_comment_db(db, comment_id)  
        
        if not result:
            raise HTTPException(status_code=500, detail="Failed to delete comment")
        
        return True
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete comment: {str(e)}")
        raise HTTPException(status_code=500, detail="Error deleting comment")