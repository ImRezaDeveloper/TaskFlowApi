from fastapi.testclient import TestClient
import sys
from pathlib import Path

# اضافه کردن مسیر ریشه
root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(root))

# from main import app
from src.taskflow.main import app

client = TestClient(app)

def test_create_user_success():
    user_data = {
        "username": "reza",
        "email": "reza@example.com",
        "hashed_password": "StrongPassword123!",
        "full_name": "rezapapi",
        "is_active": "true",
        "is_verfied": "false"
    }

    response = client.post(
        "/users/",
        json=user_data
    )

    # چاپ کردن خطا برای دیباگ
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())  # این خط رو اضافه کن
    
    assert response.status_code == 201