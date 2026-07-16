from uuid import uuid4, UUID

from fastapi.testclient import TestClient
from src.taskflow.main import app

client = TestClient(app)

# def test_create_user_success():
#     user_data = {
#         "username": "fardad",
#         "email": f"{uuid4().hex[:8]}@example.com",
#         "password": "StrongPassword123!",
#         "full_name": "rezapapi",
#         "is_active": True,
#         "is_verified": False
#     }

#     response = client.post(
#         "/users/",
#         json=user_data
#     )

#     # چاپ کردن خطا برای دیباگ
#     print("Status Code:", response.status_code)
#     print("Response JSON:", response.json())  # این خط رو اضافه کن
    
#     assert response.status_code == 201
    
# def test_get_user_success():
    
#     user_data = {
#         "username": "sina",
#         "email": "sina@test.com",
#         "password": "StrongPassword123!",
#         "full_name": "Sina",
#         "is_active": True,
#         "is_verified": False,
#     }

#     create_response = client.post(
#         "/users/",
#         json=user_data
#     )
#     # print(create_response.text)
    
#     print(create_response.json())

#     assert create_response.status_code == 201

#     user_id = create_response.json()["id"]

#     response = client.get(f"/users/{user_id}")

#     assert response.status_code == 200
#     print(create_response.status_code)
#     print(create_response.json())
#     assert response.json()["id"] == user_id
#     assert response.json()["username"] == "sina"
    
# def test_update_user_success():
    
#     # arrange
#     user_data = {
#         "username": "fardad",
#         "email": "fardad@test.com",
#         "password": "StrongPassword423!",
#         "full_name": "Fardad",
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
    
#     user_update = {
#         "username": "nima",
#         "password": "nima123Strong@password"
#     }

#     response = client.put(f"/users/{user_id}", json=user_update)
    
#     assert response.status_code == 200
#     print(create_response.status_code)
#     print(create_response.json())
    
#     assert response.json()["id"] == user_id
#     assert response.json()["username"] == "nima"
    
def test_delete_user_success():
    
    # arrange
    user_data = {
        "username": "fardad",
        "email": "fardad@test.com",
        "password": "StrongPassword423!",
        "full_name": "Fardad",
        "is_active": True,
        "is_verified": False,
    }

    create_response = client.post(
        "/users/",
        json=user_data
    )
    
    print(create_response.json())
    
    assert create_response.status_code == 201

    user_id = create_response.json()["id"]
    
    # act
    response = client.delete(f'/users/{user_id}')
    assert response.status_code == 204
    
    get_response = client.get(f'/users/{user_id}')
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "User Not Found"
    print(create_response.status_code)
    print(create_response.json())