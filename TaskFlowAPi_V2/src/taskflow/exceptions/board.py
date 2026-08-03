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
