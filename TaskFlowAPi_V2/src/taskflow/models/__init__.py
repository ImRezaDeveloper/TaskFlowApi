from src.taskflow.db.database import Base
from .users import User
from .tasks import Task
from .boards import Board
from .comments import Comment
#from .roles import Roles


# حالا مدل‌ها رو ایمپورت کن تا به Base متصل بشن

__all__ = [
    "Base",
    "User",
    "Board",
    "Task",
    "Comment",
    #"Roles"
]

