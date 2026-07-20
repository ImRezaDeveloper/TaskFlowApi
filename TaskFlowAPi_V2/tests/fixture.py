import pytest

@pytest.fixture
def auth_headers(client):
    user_data = {
        "username": "vahid",
        "email": "vahid@test.com",
        "password": "vahid123"
    }

    # Register
    client.post("/users/", json=user_data)

    # Login
    response = client.post(
        "/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }