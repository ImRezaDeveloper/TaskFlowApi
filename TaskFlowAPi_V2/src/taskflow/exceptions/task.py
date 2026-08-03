from uuid import UUID

from .base import TaskFlowException


class TaskNotFoundError(TaskFlowException):
    def __init__(self, task_id: UUID):
        super().__init__(f"task {task_id} does not exists")


class TaskPermissionDenied(TaskFlowException):
    def __init__(self, user_id: UUID):
        self.user_id = user_id
        super().__init__(f"Access denied for user with id {user_id}")


class TaskNotFoundAllError(TaskFlowException):
    def __init__(self, tasks):
        super().__init__("there was an error to get all tasks")


class TaskCreationError(TaskFlowException):
    def __init__(self, reason):
        self.reason = reason
        self.message = f"Failed to create task: {reason}"
        super().__init__(self.message)


class TasksOfBoardsNotFound(TaskFlowException):
    def __init__(self, board_id: UUID, skip: int, limit: int, reason):
        self.board_id = board_id
        self.skip = skip
        self.limit = limit
        self.reason = reason
        self.message = f"there is no tasks in the board {board_id}"
        super().__init__(self.message)


class TaskUpdateError(TaskFlowException):
    def __init__(self, task_id, reason):
        self.task_id = task_id
        self.reason = reason
        self.message = f"Failed to update task {task_id}: {reason}"
        super().__init__(self.message)

class TaskDeleteError(TaskFlowException):
    def __init__(self, task_id, reason):
        self.task_id = task_id
        self.reason = reason
        self.message = f"Failed to delete task {task_id}: {reason}"
        super().__init__(self.message)