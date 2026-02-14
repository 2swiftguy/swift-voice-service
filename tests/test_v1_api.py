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


def test_classify_intent_endpoint_with_valid_schema():
    token = os.environ["PYTHON_VOICE_TOKEN"]
    response = client.post(
        "/v1/classify-intent",
        headers={"X-Service-Token": token, "X-Trace-Id": "trace-test"},
        json={"text": "I need help resetting my password"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "intent" in body
    assert "confidence" in body
    assert response.headers["X-Trace-Id"] == "trace-test"


def test_generate_reply_schema_validation_rejects_unknown_fields():
    token = os.environ["PYTHON_VOICE_TOKEN"]
    response = client.post(
        "/v1/generate-reply",
        headers={"X-Service-Token": token},
        json={"text": "hello", "unknown": "nope"},
    )
    assert response.status_code == 422


def test_health_endpoint_uses_versioned_response_shape():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body == {"ok": True, "status": "healthy", "version": "v1"}
    assert "X-Trace-Id" in response.headers
