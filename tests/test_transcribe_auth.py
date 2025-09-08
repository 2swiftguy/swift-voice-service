import os
import sys

from fastapi.testclient import TestClient
from twilio.request_validator import RequestValidator

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SERVICE_AUTH_TOKEN", "test-token")
os.environ.setdefault("TWILIO_AUTH_TOKEN", "test-twilio-token")

from main import app

client = TestClient(app)


def test_transcribe_without_signature_returns_401():
    response = client.post("/transcribe", data={"SpeechResult": "hello"})
    assert response.status_code == 401


def test_transcribe_with_valid_signature_returns_200():
    validator = RequestValidator(os.environ["TWILIO_AUTH_TOKEN"])
    url = str(client.base_url) + "/transcribe"
    data = {"SpeechResult": "hello"}
    signature = validator.compute_signature(url, data)
    response = client.post(
        "/transcribe",
        data=data,
        headers={"X-Twilio-Signature": signature},
    )
    assert response.status_code == 200
