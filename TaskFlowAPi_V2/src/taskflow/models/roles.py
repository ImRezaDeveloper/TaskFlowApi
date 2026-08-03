from sqlalchemy import Column, ForeignKey, Integer, String

from src.taskflow.db.database import Base


class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    role_type = Column(String, index=True)

    # user
    users_id = Column(Integer, ForeignKey("users.id"), nullable=False)
