from fastapi.testclient import TestClient

from src.taskflow.main import app

client = TestClient(app)

# successfull test!
# def test_create_task_success(client, auth_headers):
#     user_id = auth_headers["user_id"]

#     # board
#     board_data = {
#         "name": "daily english",
#         "description": "this board has created for plannig your tasks",
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

#     task_data = {
#         "title": "learn english",
#         "description": "learnig english with tifani",
#         "status": "in_progress",
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

#     assert response.status_code == 201

# successfull test!
# def test_get_task_success(client, auth_headers):
#     user_id = auth_headers["user_id"]

#     # board
#     board_data = {
#         "name": "daily english",
#         "description": "this board has created for plannig your tasks",
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
#         "title": "learn english",
#         "description": "learnig english with tifani",
#         "status": "in_progress",
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

#     assert response.status_code == 201

#     # assert
#     task_id = response.json()['id']

#     task = client.get(f'/tasks/{task_id}', headers=auth_headers)

#     assert task.status_code == 200
#     print(task.status_code)
#     print(task.json())
#     assert task.json()["id"] == task_id
#     assert response.json()["title"] == "learn english"

# successfull test!
# def test_update_task_success(client, auth_headers):
#     user_id = auth_headers["user_id"]

#     # board
#     board_data = {
#         "name": "daily english",
#         "description": "this board has created for plannig your tasks",
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
#         "title": "learn english",
#         "description": "learnig english with tifani",
#         "status": "in_progress",
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

#     assert response.status_code == 201

#     # assert
#     task_id = response.json()['id']

#     update_task = {
#         "title": "learn english with me",
#         "description": "updated description"
#     }

#     task = client.patch(f'/tasks/{task_id}', headers=auth_headers, json=update_task)

#     assert task.status_code == 200
#     print(task.status_code)
#     print(task.json())
#     assert task.json()["id"] == task_id
#     assert task.json()["title"] == "learn english with me"

# successfull test ****
# def test_delete_task_success(client, auth_headers):

#     user_id = auth_headers["user_id"]

#     # board
#     board_data = {
#         "name": "daily english",
#         "description": "this board has created for plannig your tasks",
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
#         "title": "learn english",
#         "description": "learnig english with tifani",
#         "status": "in_progress",
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

#     assert response.status_code == 201

#     # assert
#     task_id = response.json()['id']

#     task = client.delete(f'/tasks/{task_id}', headers=auth_headers)

#     assert task.status_code == 204
#     print(task.status_code)

#     get_response = client.get(f'/tasks/{task_id}', headers=auth_headers)
#     print("GET Status Code:", get_response.status_code)
#     # print("GET Response JSON:", get_response.json())

#     # The task should not exist → 404 Not Found
#     assert get_response.status_code == 404
#     assert get_response.json()["detail"] == "your current task not found!"
