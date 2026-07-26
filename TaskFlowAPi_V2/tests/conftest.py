# tests/conftest.py
from httpx import AsyncClient, ASGITransport
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from src.taskflow.main import app
from src.taskflow.db.database import Base, get_db
from src.taskflow.core.config import settings
from tests.fixture.auth_headers import auth_headers

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

@pytest.fixture(scope="function")
def client():
    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()

# @pytest.fixture
# def test_db_session(test_engine):
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
#     session = SessionLocal()
#     yield session
#     session.rollback()
#     session.close()

@pytest.fixture
def sample_board(client, auth_headers):
    board_data = {
        "name": "Gym",
        "description": "this board has created for planning for exercise in gym (chest, arm,...)",
    }
    response = client.post("/boards/", json=board_data, headers=auth_headers)
    assert response.status_code == 201, f"Board creation failed: {response.json()}"
    board_id = response.json()['id']
    return {
        "board_id": board_id
    }

@pytest.fixture
def sample_task(client, auth_headers, sample_board):

    user_id = auth_headers['user_id']
    board_id = sample_board['board_id']

    task_data = {
        "title": "chest program",
        "description": "chest program for Reza",
        "status": "todo",
        "priority": "high",
        "due_date": "2026-07-10 14:47:03.397",
        "user_id": user_id,
        "board_id": board_id
    }

    response = client.post("/tasks/", json=task_data, headers=auth_headers)
    assert response.status_code == 201, f"Task creation failed: {response.json()}"
    task_id = response.json()['id']
    return {
        "task_id": task_id
    }

@pytest.fixture
def create_comment(client, auth_headers, sample_board, sample_task):

    board_id = sample_board['board_id']
    task_id = sample_task['task_id']

    comment_data = {
            "content": "oh, i love this program, it gave me the heavy weight",
    }
        
    new_commment = client.post('/comments/', json=comment_data, headers=auth_headers, params={
        "task_id": f'{task_id}',
        "board_id": f'{board_id}'
    })
        
    print("Status Code:", new_commment.status_code)
    print("Response JSON:", new_commment.json())
        
    comment_id = new_commment.json()['id']
        
    assert new_commment.status_code == 201
    assert new_commment.json()["content"] == "oh, i love this program, it gave me the heavy weight"

    return {
        'comment_id': comment_id
    }