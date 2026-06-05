from fastapi import APIRouter
from taskflow.app.users.user_repository import get_users

router = APIRouter()

@router.get("/users")
def list_users():
    return get_users()