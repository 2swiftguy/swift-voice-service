import os
import sys

from pydantic import ValidationError

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

os.environ.setdefault("TWILIO_SID", "test-twilio-sid")
os.environ.setdefault("TWILIO_TOKEN", "test-twilio-token")
os.environ.setdefault("PYTHON_VOICE_TOKEN", "test-voice-token")
os.environ.setdefault("PYTHON_SMS_TOKEN", "test-sms-token")

from app.models.contracts import SmsRequest, VoiceRequest


def test_sms_contract_requires_message_sid():
    try:
        SmsRequest.model_validate({"from": "+1", "to": "+2", "trace_id": "trace-1"})
        raised = False
    except ValidationError:
        raised = True

    assert raised


def test_voice_contract_uses_laravel_payload_shape():
    payload = VoiceRequest.model_validate(
        {
            "from": "+1",
            "to": "+2",
            "call_sid": "CA123",
            "trace_id": "trace-1",
        }
    )

    assert payload.from_ == "+1"
    assert payload.call_sid == "CA123"
