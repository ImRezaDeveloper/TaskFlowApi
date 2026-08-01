from uuid import UUID
from .base import TaskFlowException

class TaskNotFoundError(TaskFlowException):

    def __init__(self, task_id: UUID):
        super().__init__(f"task {task_id} does not exists")
