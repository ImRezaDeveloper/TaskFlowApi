import pytest
from fastapi.testclient import TestClient
from src.taskflow.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
            
    
@pytest.fixture
def sample_board(client, auth_headers):
    board_data = {
        "name": "Gym",
        "description": "this board has created for plannig for excersise in gym (chest, arm,...)",
    }
    response = client.post("/boards/", json=board_data, headers=auth_headers)
    assert response.status_code == 201
    return response.json()["id"]  # board_id

@pytest.fixture
def sample_board(client, auth_headers):
    board_data = {
        "name": "Gym",
        "description": "this board has created for plannig for excersise in gym (chest, arm,...)",
    }
    response = client.post("/boards/", json=board_data, headers=auth_headers)
    assert response.status_code == 201
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
    assert response.status_code == 201
    return response.json()["id"]