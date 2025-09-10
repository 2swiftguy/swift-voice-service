import os
import sys

from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

os.environ.setdefault("TWILIO_SID", "test-twilio-sid")
os.environ.setdefault("TWILIO_TOKEN", "test-twilio-token")

os.environ.setdefault("PYTHON_VOICE_TOKEN", "test-voice-token")
os.environ.setdefault("PYTHON_SMS_TOKEN", "test-sms-token")


from main import app

client = TestClient(app)


def test_sms_without_token_returns_401():
    response = client.post("/sms")
    assert response.status_code == 401


def test_sms_with_token_returns_200():
    token = os.environ["PYTHON_SMS_TOKEN"]
    response = client.post("/sms", headers={"X-Service-Token": token})
    assert response.status_code == 200
