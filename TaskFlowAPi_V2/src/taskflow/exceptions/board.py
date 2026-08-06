from uuid import UUID

from .base import TaskFlowException


class BoardNotFoundError(TaskFlowException):
    def __init__(self, board_id: UUID):
        self.board_id = board_id
        super().__init__(f"Board {board_id} does not found!")


class BoardPermissionDenied(TaskFlowException):
    def __init__(self, ownder_id: UUID):
        self.owner_id = ownder_id
        super().__init__(f"Access denied for owner with id {ownder_id}")


class BoardCreationError(TaskFlowException):
    def __init__(self, reason):
        self.reason = reason
        self.message = f"Failed to create board {reason}"
        super().__init__(self.message)


class BoardAlreadyExistError(TaskFlowException):
    def __init__(self, board_name: str, current_user_id: UUID):
        self.board_name = board_name
        self.user_id = current_user_id
        self.message = f"board '{board_name}' already exist: user {current_user_id}"
        super().__init__(self.message)
