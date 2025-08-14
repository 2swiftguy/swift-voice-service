from app.core.settings import settings
from app.services.state import set_state

def build_initial_twiml(payload: dict) -> str:
    sid = payload.get("CallSid") or ""
    set_state(sid, stage="gather")

    base = settings.PUBLIC_BASE_URL or ""
    partial_cb = f'{base}/partial' if base else ""

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<Response>',
        f'  <Gather input="speech dtmf" action="/transcribe" method="POST" speechTimeout="auto"'
        + (f' partialResultCallback="{partial_cb}" partialResultCallbackMethod="POST"' if partial_cb else '')
        + ' bargeIn="true">',
        '    <Say voice="Polly.Matthew">Welcome to SWIFT Voice. You can interrupt me at any time. What do you need?</Say>',
        '  </Gather>',
        '  <Say voice="Polly.Matthew">I did not catch that. Goodbye.</Say>',
        '</Response>'
    ]
    return "\n".join(parts)

def build_transcribe_twiml(payload: dict) -> str:
    text = payload.get("SpeechResult") or ""
    resp = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<Response>',
        f'  <Say voice="Polly.Matthew">You said: {text}</Say>',
        '  <Hangup/>',
        '</Response>'
    ]
    return "\n".join(resp)