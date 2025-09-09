import os
import sys

from fastapi.testclient import TestClient

# Allow imports from project root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Ensure required environment variables are set for settings
os.environ.setdefault("SERVICE_AUTH_TOKEN", "test-token")

os.environ.setdefault("TWILIO_SID", "test-twilio-sid")
os.environ.setdefault("TWILIO_TOKEN", "test-twilio-token")


os.environ.setdefault("PYTHON_VOICE_TOKEN", "test-voice-token")
os.environ.setdefault("PYTHON_SMS_TOKEN", "test-sms-token")


from main import app

client = TestClient(app)


def test_process_call_without_token_returns_401():
    response = client.post("/process-call", json={})
    assert response.status_code == 401


def test_process_call_with_token_returns_200():
    token = os.environ["PYTHON_VOICE_TOKEN"]
    response = client.post("/process-call", headers={"X-Service-Token": token}, json={})
    assert response.status_code == 200
