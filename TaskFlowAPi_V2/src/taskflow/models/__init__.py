from src.taskflow.db.database import Base

from .boards import Board
from .comments import Comment
from .tasks import Task
from .users import User

# from .roles import Roles


# حالا مدل‌ها رو ایمپورت کن تا به Base متصل بشن

__all__ = [
    "Base",
    "Board",
    "Comment",
    "Task",
    "User",
    # "Roles"
]
