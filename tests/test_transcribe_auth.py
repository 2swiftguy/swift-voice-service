import os
import sys

from fastapi.testclient import TestClient
from twilio.request_validator import RequestValidator

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SERVICE_AUTH_TOKEN", "test-token")
os.environ.setdefault("TWILIO_SID", "test-twilio-sid")
os.environ.setdefault("TWILIO_TOKEN", "test-twilio-token")

from main import app

client = TestClient(app)


def test_transcribe_without_signature_returns_401():
    data = {"SpeechResult": "hello", "AccountSid": os.environ["TWILIO_SID"]}
    response = client.post("/transcribe", data=data)
    assert response.status_code == 401


def test_transcribe_with_valid_signature_returns_200():
    validator = RequestValidator(os.environ["TWILIO_TOKEN"])
    url = str(client.base_url) + "/transcribe"
    data = {
        "SpeechResult": "hello",
        "AccountSid": os.environ["TWILIO_SID"],
    }
    signature = validator.compute_signature(url, data)
    response = client.post(
        "/transcribe",
        data=data,
        headers={"X-Twilio-Signature": signature},
    )
    assert response.status_code == 200


def test_transcribe_with_invalid_account_returns_401():
    validator = RequestValidator(os.environ["TWILIO_TOKEN"])
    url = str(client.base_url) + "/transcribe"
    data = {
        "SpeechResult": "hello",
        "AccountSid": "wrong-sid",
    }
    signature = validator.compute_signature(url, data)
    response = client.post(
        "/transcribe",
        data=data,
        headers={"X-Twilio-Signature": signature},
    )
    assert response.status_code == 401
