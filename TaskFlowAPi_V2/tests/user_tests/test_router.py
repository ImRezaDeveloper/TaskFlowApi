from fastapi.testclient import TestClient

from src.taskflow.main import app

client = TestClient(app)

# successfull test!
# def test_create_user_success(client):

#     user_data = {
#         "username": "shakiba",
#         "email": f"{uuid4().hex[:8]}@test.com",
#         "password": "StrongPassword123!",
#         "full_name": "shakiba",
#         "is_active": True,
#         "is_verified": False
#     }

#     response = client.post(
#         "/users/",
#         json=user_data
#     )

#     print("Status Code:", response.status_code)
#     print("Response JSON:", response.json())

#     assert response.status_code == 201

# successfull test!
# def test_get_user_success(client):

#     user_data = {
#         "username": "sima",
#         "email": "sima@test.com",
#         "password": "StrongPassword123!",
#         "full_name": "sima",
#         "is_active": True,
#         "is_verified": False,
#     }

#     create_response = client.post("/users/", json=user_data)

#     assert create_response.status_code == 201

#     user_id = create_response.json()["id"]

#     response = client.get(f"/users/{user_id}")

#     assert response.status_code == 200
#     assert response.json()["id"] == user_id
#     assert response.json()["username"] == "sima"

# successfull test!
# def test_update_user_success(client):
#     user_data = {
#         "username": "shokoh",
#         "email": "shokoh@test.com",
#         "password": "StrongPassword423!",
#         "full_name": "shokoh",
#         "is_active": True,
#         "is_verified": False,
#     }

#     create_response = client.post("/users/", json=user_data)
#     assert create_response.status_code == 201
#     user_id = create_response.json()["id"]

#     user_update = {
#         "username": "nima",
#         "password": "nima123Strong@password"
#     }
#     update_response = client.put(f"/users/{user_id}", json=user_update)

#     assert update_response.status_code == 200
#     updated_user = update_response.json()
#     assert updated_user["id"] == user_id
#     assert updated_user["username"] == "nima"

# successfull test!
# def test_delete_user_success(client):

#     # arrange
#     user_data = {
#         "username": "farshad",
#         "email": "farshad@test.com",
#         "password": "StrongPassword423!",
#         "full_name": "farshad",
#         "is_active": True,
#         "is_verified": False,
#     }

#     create_response = client.post(
#         "/users/",
#         json=user_data
#     )

#     print(create_response.json())

#     assert create_response.status_code == 201

#     user_id = create_response.json()["id"]

#     # act
#     response = client.delete(f'/users/{user_id}')
#     assert response.status_code == 204

#     get_response = client.get(f'/users/{user_id}')
#     assert get_response.status_code == 404
#     assert get_response.json()["detail"] == "User not found"
#     print(create_response.status_code)
