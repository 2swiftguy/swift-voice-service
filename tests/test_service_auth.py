import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

os.environ.setdefault("TWILIO_SID", "test-twilio-sid")
os.environ.setdefault("TWILIO_TOKEN", "test-twilio-token")
os.environ.setdefault("PYTHON_VOICE_TOKEN", "test-voice-token")
os.environ.setdefault("PYTHON_SMS_TOKEN", "test-sms-token")

from app.core.auth import service_token_matches


def test_service_token_matches_expected_token():
    assert service_token_matches("test-voice-token", "test-voice-token")


def test_service_token_rejects_missing_or_wrong_token():
    assert not service_token_matches(None, "test-voice-token")
    assert not service_token_matches("wrong-token", "test-voice-token")
