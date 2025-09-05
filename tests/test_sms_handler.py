import os
import sys

from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SERVICE_AUTH_TOKEN", "test-token")

from main import app

client = TestClient(app)


def test_sms_route_returns_twiml():
    response = client.post("/sms")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/xml")
    assert "<Response>" in response.text
    assert "</Response>" in response.text

