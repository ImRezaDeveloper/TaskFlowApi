import pytest
from fastapi.testclient import TestClient
from src.taskflow.main import app  # حالا کار می‌کنه


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c