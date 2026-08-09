from uuid import UUID

from pydantic import EmailStr

from .base import TaskFlowException


class UserNotFoundError(TaskFlowException):
    def __init__(self, user_id: UUID):
        self.user_id = user_id
        super().__init__(f"user {user_id} does not exists")

class UserDeleteError(TaskFlowException):
    def __init__(self, user_id: UUID, reason: str):
        self.user_id = user_id
        self.reason = reason
        super().__init__(f"Falied to delete user {user_id}", reason)

class EmailAlreadyExistError(TaskFlowException):
    def __int__(self, email: EmailStr):
        self.email = email
        super().__init__(f"email {email} already exists")


class UserAlreadyExistError(TaskFlowException):
    def __int__(self, username: str):
        self.username = username
        super().__init__(f"user : {username}, already exists")


class UserCreationError(TaskFlowException):
    def __init__(self, username: str, email: str, reason: str):
        self.username = username
        self.email = email
        self.reason = reason
        self.message = f"Failed to create user {username} ({email}): {reason}"
        super().__init__(self.message)


class UserMustBeLoggedIn(TaskFlowException):
    def __init__(self, current_user_id: UUID, reason: str):
        self.user_id = current_user_id
        self.reason = reason
        self.message = "You must be logged in to create a board"
        super().__init__(self.message)
