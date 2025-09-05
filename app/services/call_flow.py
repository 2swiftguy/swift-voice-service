from app.core.settings import settings
from app.services.state import set_state
from twilio.twiml.voice_response import VoiceResponse


def build_initial_twiml(payload: dict) -> str:
    sid = payload.get("CallSid") or ""
    set_state(sid, stage="gather")

    base = settings.PUBLIC_BASE_URL or ""
    partial_cb = f"{base}/partial" if base else ""

    response = VoiceResponse()
    gather_kwargs = {
        "input": "speech dtmf",
        "action": "/transcribe",
        "method": "POST",
        "speech_timeout": "auto",
        "barge_in": True,
    }
    if partial_cb:
        gather_kwargs["partial_result_callback"] = partial_cb
        gather_kwargs["partial_result_callback_method"] = "POST"

    gather = response.gather(**gather_kwargs)
    gather.say(
        "Welcome to SWIFT Voice. You can interrupt me at any time. What do you need?",
        voice="Polly.Matthew",
    )
    response.say("I did not catch that. Goodbye.", voice="Polly.Matthew")
    return str(response)


def build_transcribe_twiml(payload: dict) -> str:
    text = payload.get("SpeechResult") or ""
    response = VoiceResponse()
    response.say(f"You said: {text}", voice="Polly.Matthew")
    response.hangup()
    return str(response)
