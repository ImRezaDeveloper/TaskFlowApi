# taskflow/app/tests/conftest.py
import sys
from pathlib import Path

# اضافه کردن مسیر ریشه پروژه (جایی که main.py هست)
root_path = Path(__file__).parent.parent.parent.parent  # از tests به ریشه
sys.path.insert(0, str(root_path))

import pytest
from fastapi.testclient import TestClient
from main import app  # حالا کار می‌کنه


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c