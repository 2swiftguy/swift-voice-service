from fastapi import APIRouter, Depends, Header, HTTPException

from app.core.settings import settings
from app.models.api_v1 import (
    ClassifyIntentRequestV1,
    ClassifyIntentResponseV1,
    GenerateReplyRequestV1,
    GenerateReplyResponseV1,
    HealthResponseV1,
    ReadyResponseV1,
    StreamingPartialRequestV1,
    StreamingPartialResponseV1,
    StreamingSessionRequestV1,
    StreamingSessionResponseV1,
    TranscribeRequestV1,
    TranscribeResponseV1,
)
from app.services.ai_worker import classify_intent, generate_reply
from app.services.streaming_sessions import create_streaming_session, update_partial

router = APIRouter(prefix="/v1", tags=["v1"])


def require_voice_token(x_service_token: str | None = Header(None)) -> None:
    if x_service_token != settings.PYTHON_VOICE_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.post("/transcribe", response_model=TranscribeResponseV1)
async def transcribe(payload: TranscribeRequestV1, _: None = Depends(require_voice_token)) -> TranscribeResponseV1:
    transcript = payload.text.strip()
    return TranscribeResponseV1(transcript=transcript)


@router.post("/classify-intent", response_model=ClassifyIntentResponseV1)
async def classify(payload: ClassifyIntentRequestV1, _: None = Depends(require_voice_token)) -> ClassifyIntentResponseV1:
    intent, confidence = await classify_intent(payload.text)
    return ClassifyIntentResponseV1(intent=intent, confidence=confidence)


@router.post("/generate-reply", response_model=GenerateReplyResponseV1)
async def reply(payload: GenerateReplyRequestV1, _: None = Depends(require_voice_token)) -> GenerateReplyResponseV1:
    reply_text = await generate_reply(payload.text, payload.intent)
    return GenerateReplyResponseV1(reply=reply_text)


@router.get("/streaming")
async def streaming_info() -> dict:
    return {"status": "ok", "version": "v1"}


@router.post("/streaming/sessions", response_model=StreamingSessionResponseV1)
async def create_session(payload: StreamingSessionRequestV1, _: None = Depends(require_voice_token)) -> StreamingSessionResponseV1:
    session_id, ttl_seconds = create_streaming_session(payload.call_sid, payload.stage)
    return StreamingSessionResponseV1(session_id=session_id, ttl_seconds=ttl_seconds)


@router.post("/streaming/partial", response_model=StreamingPartialResponseV1)
async def streaming_partial(payload: StreamingPartialRequestV1, _: None = Depends(require_voice_token)) -> StreamingPartialResponseV1:
    update_partial(payload.session_id, payload.partial_text)
    return StreamingPartialResponseV1(session_id=payload.session_id)


public_router = APIRouter(tags=["public"])


@public_router.get("/health", response_model=HealthResponseV1)
def health() -> HealthResponseV1:
    return HealthResponseV1()


@public_router.get("/ready", response_model=ReadyResponseV1)
def ready() -> ReadyResponseV1:
    return ReadyResponseV1()
