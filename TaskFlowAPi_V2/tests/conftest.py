# tests/conftest.py
from httpx import AsyncClient, ASGITransport
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from src.taskflow.main import app
from src.taskflow.db.database import Base, get_db
from src.taskflow.core.config import settings
from sqlalchemy import create_engine
import pytest_asyncio

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:rezapapi1384@localhost:5433/test_db"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Sprint 3
# @pytest.fixture
# async def db_session():

#     async with test_engine.connect() as connection:

#         transaction = await connection.begin()

#         # Session روی همین connection
#         session = AsyncSession(bind=connection, expire_on_commit=False)

#         yield session

#         # 🔥 این مهم‌ترین خطه
#         await transaction.rollback()

#         await session.close()

# @pytest.fixture(scope="session", autouse=True)
# def prepare_database():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)

#     yield

#     Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():

    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()

@pytest.fixture(scope="session")
def auth_headers(client):
    user_data = {
        "username": "vahid",
        "email": "vahid@test.com",
        "password": "StrongPassword123!",
        "full_name": "Vahid",
        "is_active": True,
        "is_verified": False
    }
    register_response = client.post("/users/", json=user_data)
    if register_response.status_code != 201:
        raise Exception(f"User registration failed: {register_response.json()}")

    login_data = {
        "username": "vahid@test.com",
        "password": "StrongPassword123!"
    }
    login_response = client.post("/auth/login", json=login_data)
    if login_response.status_code != 200:
        raise Exception(f"Login failed: {login_response.json()}")
    
    access_token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def sample_board(client, auth_headers):
    board_data = {
        "name": "Gym",
        "description": "this board has created for planning for exercise in gym (chest, arm,...)",
    }
    response = client.post("/boards/", json=board_data, headers=auth_headers)
    assert response.status_code == 201, f"Board creation failed: {response.json()}"
    return response.json()["id"]

@pytest.fixture
def sample_task(client, auth_headers, sample_board):
    user_data = {
        "username": "fardad",
        "email": "fardad@test.com",
        "password": "StrongPassword123!",
        "full_name": "Fardad",
        "is_active": True,
        "is_verified": False
    }
    user_response = client.post("/users/", json=user_data)
    user_id = user_response.json()["id"]

    task_data = {
        "title": "chest program",
        "description": "chest program for Reza",
        "status": "todo",
        "priority": "high",
        "due_date": "2026-07-10 14:47:03.397",
        "user_id": user_id,
        "board_id": sample_board
    }
    response = client.post("/tasks/", json=task_data, headers=auth_headers)
    assert response.status_code == 201, f"Task creation failed: {response.json()}"
    return response.json()["id"]