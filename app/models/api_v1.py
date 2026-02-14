from pydantic import BaseModel, ConfigDict, Field


class APIModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class HealthResponseV1(APIModel):
    ok: bool = True
    status: str = "healthy"
    version: str = "v1"


class ReadyResponseV1(APIModel):
    ok: bool = True
    status: str = "ready"
    version: str = "v1"


class TranscribeRequestV1(APIModel):
    text: str = Field(..., min_length=1, description="Speech text or transcript input")
    locale: str | None = Field(default="en-US")


class TranscribeResponseV1(APIModel):
    transcript: str
    model: str = "v1"


class ClassifyIntentRequestV1(APIModel):
    text: str = Field(..., min_length=1)


class ClassifyIntentResponseV1(APIModel):
    intent: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    model: str = "rules-v1"


class GenerateReplyRequestV1(APIModel):
    text: str = Field(..., min_length=1)
    intent: str | None = None


class GenerateReplyResponseV1(APIModel):
    reply: str
    model: str = "template-v1"


class StreamingSessionRequestV1(APIModel):
    call_sid: str = Field(..., min_length=1)
    stage: str = Field(default="gather")


class StreamingSessionResponseV1(APIModel):
    session_id: str
    ttl_seconds: int
    status: str = "created"


class StreamingPartialRequestV1(APIModel):
    session_id: str = Field(..., min_length=1)
    partial_text: str = Field(..., min_length=1)


class StreamingPartialResponseV1(APIModel):
    ok: bool = True
    session_id: str
