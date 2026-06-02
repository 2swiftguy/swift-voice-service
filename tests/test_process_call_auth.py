import os
import sys

from fastapi.testclient import TestClient

# Allow imports from project root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Ensure required environment variables are set for settings
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
    response = client.post(
        "/process-call",
        headers={"X-Service-Token": token, "X-Trace-Id": "trace-voice"},
        json={
            "from": "+15550001111",
            "to": "+15550002222",
            "call_sid": "CA123",
            "trace_id": "trace-voice",
        },
    )
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/xml")


def test_process_call_validation_error_matches_laravel_contract():
    token = os.environ["PYTHON_VOICE_TOKEN"]
    response = client.post(
        "/process-call",
        headers={"X-Service-Token": token, "X-Trace-Id": "trace-voice"},
        json={"from": "+15550001111"},
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "validation_error"
    assert response.json()["error"]["message"] == "Invalid voice payload"
    assert response.json()["error"]["trace_id"] == "trace-voice"
