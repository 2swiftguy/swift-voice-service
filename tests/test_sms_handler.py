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


def test_sms_route_returns_twiml():
    token = os.environ["PYTHON_SMS_TOKEN"]
    response = client.post("/sms", headers={"X-Service-Token": token})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/xml")
    assert "<Response>" in response.text
    assert "</Response>" in response.text


def test_process_sms_accepts_laravel_contract_payload():
    token = os.environ["PYTHON_SMS_TOKEN"]
    response = client.post(
        "/process-sms",
        headers={"X-Service-Token": token, "X-Trace-Id": "trace-sms"},
        json={
            "from": "+15550001111",
            "to": "+15550002222",
            "body": "hello",
            "message_sid": "SM123",
            "trace_id": "trace-sms",
        },
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/xml")
    assert "SM123" in response.text


def test_process_sms_validation_error_matches_laravel_contract():
    token = os.environ["PYTHON_SMS_TOKEN"]
    response = client.post(
        "/process-sms",
        headers={"X-Service-Token": token, "X-Trace-Id": "trace-sms"},
        json={"from": "+15550001111"},
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "validation_error"
    assert response.json()["error"]["message"] == "Invalid SMS payload"
    assert response.json()["error"]["trace_id"] == "trace-sms"
