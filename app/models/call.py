"""Models for call-related payloads."""

from pydantic import BaseModel, Field


class CallPayload(BaseModel):
    """Payload sent by Twilio during voice interactions."""

    from_: str | None = Field(None, alias="From")
    to: str | None = Field(None, alias="To")
    call_sid: str | None = Field(None, alias="CallSid")
    speech_result: str | None = Field(None, alias="SpeechResult")

