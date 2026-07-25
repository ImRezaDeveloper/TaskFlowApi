import pytest
from fastapi.testclient import TestClient
from src.taskflow.main import app

@pytest.fixture(scope="function")
def auth_headers(client):
    user_data = {
        "username": "vahid",
        "email": "vahid@test.com",
        "password": "vahid123",
        "full_name": "Vahid",
        "is_active": True,
        "is_verified": False
    }

    register_response = client.post("/users/", json=user_data)
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}

    user_response = client.get("/users/me", headers=headers)
    assert user_response.status_code == 200
    user_id = user_response.json()["id"]

    return {
        "Authorization": f"Bearer {token}",
        "user_id": user_id
    }