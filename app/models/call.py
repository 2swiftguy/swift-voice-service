from pydantic import BaseModel
class CallPayload(BaseModel):
    From: str | None = None
    To: str | None = None
    CallSid: str | None = None
    SpeechResult: str | None = None