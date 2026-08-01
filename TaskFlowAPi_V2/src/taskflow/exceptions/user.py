from uuid import UUID
from .base import TaskFlowException

class UserNotFoundError(TaskFlowException):

    def __init__(self, user_id: UUID):
        super().__init__(f"user {user_id} does not exists")

