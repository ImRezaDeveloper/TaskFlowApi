from uuid import uuid4

# successfull test
# def test_create_board_success(client, auth_headers):

#     board_data = {
#             "name": "Gym",
#             "description": "this board has created for planning for exercise in gym (chest, arm,...)",
#     }
    
#     response = client.post("/boards/", json=board_data, headers=auth_headers)
#     assert response.status_code == 201, f"Board creation failed: {response.json()}"
#     assert response.json()['name'] == board_data['name']

# successfull test
# def test_create_board_missing_name(client, auth_headers):
#     board_data = {"description": "No name here"}
    
#     response = client.post("/boards/", json=board_data, headers=auth_headers)
#     assert response.status_code == 422
#     assert "name" in str(response.json())

# successfull test
# def test_get_board_success(client, auth_headers, sample_board):
#     board_id = sample_board["board_id"]
    
#     response = client.get(f"/boards/{board_id}", headers=auth_headers)
#     assert response.status_code == 200
#     data = response.json()
    
#     assert data["id"] == board_id
#     assert data["name"] == "Gym"
#     assert data["description"] == "this board has created for planning for exercise in gym (chest, arm,...)"

# successfull test
# def test_get_board_not_found(client, auth_headers):
#     fake_id = uuid4()
    
#     response = client.get(f"/boards/{fake_id}", headers=auth_headers)
#     assert response.status_code == 404
#     assert "not found" in response.json()["detail"].lower()

# ========== 3. UPDATE ==========
# successfull test
# def test_update_board_success(client, auth_headers, sample_board):
#     board_id = sample_board["board_id"]

#     update_data = {
#         "name": "Project Beta",
#         "description": "Updated description"
#     }
    
#     response = client.put(f"/boards/{board_id}", json=update_data, headers=auth_headers)
#     assert response.status_code == 200
#     data = response.json()
    
#     assert data["name"] == update_data["name"]
#     assert data["description"] == update_data["description"]

# def test_update_board_not_found(client, auth_headers):
#     fake_id = uuid4()
#     update_data = {"name": "New Name"}
    
#     response = client.put(f"/boards/{fake_id}", json=update_data, headers=auth_headers)
#     assert response.status_code == 404

# ========== 4. DELETE ==========
# successfull test
# def test_delete_board_success(client, auth_headers, sample_board):
#     board_id = sample_board["board_id"]
    
#     delete_response = client.delete(f"/boards/{board_id}", headers=auth_headers)
#     assert delete_response.status_code == 204
    
#     get_response = client.get(f"/boards/{board_id}", headers=auth_headers)
#     assert get_response.status_code == 404

# def test_delete_board_not_found(client, auth_headers):
#     fake_id = uuid4()
    
#     response = client.delete(f"/boards/{fake_id}", headers=auth_headers)
#     assert response.status_code == 404

# successfull test
# def test_create_task_in_board_success(client, auth_headers, sample_board):
#     user_id = auth_headers["user_id"]
#     board_id = sample_board['board_id']
    
#     task_data = {
#         "title": "Learn FastAPI",
#         "description": "Complete the FastAPI tutorial",
#         "status": "todo",
#         "priority": "high",
#         "due_date": "2026-07-10 14:47:03.397",
#         "user_id": user_id,
#         "board_id": board_id
#     }
    
#     response = client.post(
#         f"/boards/{board_id}/tasks"s,
#         json=task_data,
#         headers=auth_headers
#     )
    
#     assert response.status_code == 201
#     data = response.json()
    
#     assert data["title"] == task_data["title"]
#     assert data["description"] == task_data["description"]
#     # assert data["board_id"] == board_id
#     assert data["user_id"] is not None
#     assert "id" in data


def test_create_task_in_board_not_found(client, auth_headers):
    fake_board_id = uuid4()
    task_data = {
        "title": "Learn FastAPI",
        "description": "Complete the FastAPI tutorial",
        "status": "todo",
        "priority": "high"
    }
    
    response = client.post(
        f"/boards/{fake_board_id}/tasks",
        json=task_data,
        headers=auth_headers
    )
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

