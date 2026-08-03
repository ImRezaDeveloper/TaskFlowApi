from uuid import UUID

from .base import TaskFlowException


class CommentNotFoundError(TaskFlowException):
    def __init__(self, comment_id: UUID):
        self.comment_id = comment_id
        super().__init__(f"comment {comment_id} does not found!")


class CommentPermissionDenied(TaskFlowException):
    def __init__(self, author_id: UUID):
        self.author_id = author_id
        super().__init__(f"Access denied for author with id {author_id}")


class CommentDeleteFailed(TaskFlowException):
    def __init__(self, comment_id: UUID, reason):
        self.comment_id = (comment_id,)
        self.reason = reason
        super().__init__(f"Failed to delete comment {comment_id}: reason: {reason}")


class CommentUpdateError(TaskFlowException):
    def __init__(self, comment_id, reason):
        self.comment_id = comment_id
        self.reason = reason
        self.message = f"Failed to update comment {comment_id}: {reason}"
        super().__init__(self.message)


class CommentCreateError(TaskFlowException):
    def __init__(self, reason):
        self.reason = reason
        self.message = f"Failed to create comment: {reason}"
        super().__init__(self.message)
