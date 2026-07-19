from uuid import uuid4, UUID

from fastapi.testclient import TestClient
from src.taskflow.main import app
from tests.fixture import auth_headers

client = TestClient(app)

# def test_create_comment_success(client, auth_headers):
    
#     user_data = {
#         "username": "fardad",
#         "email": "fardad@test.com",
#         "password": "StrongPassword123!",
#         "full_name": "Fadad",
#         "is_active": True,
#         "is_verified": False
#     }

#     response = client.post(
#         "/users/",
#         json=user_data
#     )

#     print("Status Code:", response.status_code)
#     print("Response JSON:", response.json())
    
#     user_id = response.json()['id']
#     assert response.status_code == 201
    
#     # board
#     board_data = {
#         "name": "Gym",
#         "description": "this board has created for plannig for excersise in gym (chest, arm,...)",
#     }

#     create_response = client.post(
#         "/boards/",
#         json=board_data,
#         headers=auth_headers
#     )

#     print("Status Code:", create_response.status_code)
#     print("Response JSON:", create_response.json())
    
#     board_id = create_response.json()['id']
    
#     assert create_response.status_code == 201
    
#     # task
#     task_data = {
#         "title": "chest program",
#         "description": "chest program for Reza",
#         "status": "todo",
#         "priority": "high",
#         "due_date": "2026-07-10 14:47:03.397",
#         "user_id": f"{user_id}",
#         "board_id": f"{board_id}"
#     }

#     response = client.post(
#         "/tasks/",
#         json=task_data,
#         headers=auth_headers
#     )

#     print("Status Code:", response.status_code)
#     print("Response JSON:", response.json())
#     task_id = response.json()['id']
    
#     assert response.status_code == 201
    
#     comment_data = {
#         "content": "oh, i love this program, it gave me the heavy weight",
#     }
    
#     new_commment = client.post('/comments/', json=comment_data, headers=auth_headers, params={
#         "task_id": f'{task_id}',
#         "board_id": f'{board_id}'
#     })
    
#     print("Status Code:", new_commment.status_code)
#     print("Response JSON:", new_commment.json())
    
#     assert new_commment.status_code == 201
#     assert new_commment.json()["content"] == "oh, i love this program, it gave me the heavy weight"

def test_get_comment_success(client, auth_headers):
    
    user_data = {
        "username": "fardad",
        "email": "fardad@test.com",
        "password": "StrongPassword123!",
        "full_name": "Fadad",
        "is_active": True,
        "is_verified": False
    }

    response = client.post(
        "/users/",
        json=user_data
    )

    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
    
    user_id = response.json()['id']
    assert response.status_code == 201
    
    # board
    board_data = {
        "name": "Gym",
        "description": "this board has created for plannig for excersise in gym (chest, arm,...)",
    }

    create_response = client.post(
        "/boards/",
        json=board_data,
        headers=auth_headers
    )

    print("Status Code:", create_response.status_code)
    print("Response JSON:", create_response.json())
    
    board_id = create_response.json()['id']
    
    assert create_response.status_code == 201
    
    # task
    task_data = {
        "title": "chest program",
        "description": "chest program for Reza",
        "status": "todo",
        "priority": "high",
        "due_date": "2026-07-10 14:47:03.397",
        "user_id": f"{user_id}",
        "board_id": f"{board_id}"
    }

    response = client.post(
        "/tasks/",
        json=task_data,
        headers=auth_headers
    )

    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
    task_id = response.json()['id']
    
    assert response.status_code == 201
    
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
    
    # assert
    comment = client.get(f'/comments/{comment_id}', headers=auth_headers)
    
    print("Status Code:", comment.status_code)
    print("Response JSON:", comment.json())
    
    assert comment.status_code == 200
    assert new_commment.json()["content"] == "oh, i love this program, it gave me the heavy weight"