from uuid import uuid4, UUID

from fastapi.testclient import TestClient
from src.taskflow.main import app
from ..conftest import auth_headers, sample_board

client = TestClient(app)

# successfull test
# def test_create_comment_success(client, auth_headers, sample_board):
    
#     user_id = auth_headers["user_id"]
#     board_id = sample_board["board_id"]
        
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

# successfull test ****
# def test_get_comment_success(client, auth_headers, sample_board):
    
#     user_id = auth_headers["user_id"]
#     board_id = sample_board["board_id"]

#         # task
#     task_data = {
#             "title": "chest program",
#             "description": "chest program for Reza",
#             "status": "todo",
#             "priority": "high",
#             "due_date": "2026-07-10 14:47:03.397",
#             "user_id": f"{user_id}",
#             "board_id": f"{board_id}"
#         }

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
    
#     comment_id = new_commment.json()['id']
    
#     assert new_commment.status_code == 201
#     assert new_commment.json()["content"] == "oh, i love this program, it gave me the heavy weight"
    
#     # assert
#     comment = client.get(f'/comments/{comment_id}', headers=auth_headers)
    
#     print("Status Code:", comment.status_code)
#     print("Response JSON:", comment.json())
    
#     assert comment.status_code == 200
#     assert new_commment.json()["content"] == "oh, i love this program, it gave me the heavy weight"

# successfull test ****
# def test_update_comment_success(client, auth_headers, sample_board, sample_task, create_comment):

#     user_id = auth_headers['user_id']
#     board_id = sample_board['board_id']
#     task_id = sample_task['task_id']

#     # comment
#     comment_id = create_comment['comment_id']

#     # update
#     update_data = {"content": "updated content"}

#     update_response = client.patch(
#         f"/comments/{comment_id}",
#         json=update_data,
#         headers=auth_headers
#     )
    
#     assert update_response.status_code == 200
#     assert update_response.json()["content"] == "updated content"

# successfull test **** 
# def test_delete_comment_success(client, auth_headers, sample_board, sample_task, create_comment):
    
#    comment_id = create_comment['comment_id']

#    delete_response = client.delete(
#        f"/comments/{comment_id}",
#        headers=auth_headers
#    )

#    assert delete_response.status_code == 204

#    get_response = client.get(
#        f"/comments/{comment_id}",
#        headers=auth_headers
#    )
#    assert get_response.status_code == 404
#    print("Response", get_response.json())