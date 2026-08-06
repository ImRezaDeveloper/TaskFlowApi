from uuid import UUID

from pydantic import EmailStr

from .base import TaskFlowException


class EmailorPasswordWrongError(TaskFlowException):
    def __init__(self, email: EmailStr, password: str):
        self.email = email
        self.password = password
        self.message = "Wrong email or password"
        super().__init__(self.message)


class CouldNotValidateCredentialsError(TaskFlowException):
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(detail=detail, headers={"WWW-Authenticate": "Bearer"})
