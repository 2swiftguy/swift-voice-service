from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from pydantic import ValidationError
from twilio.request_validator import RequestValidator

from app.core.auth import require_voice_token
from app.core.settings import settings
from app.models.contracts import ErrorEnvelope, ErrorPayload, VoiceRequest
from app.services.call_flow import build_initial_twiml, build_transcribe_twiml
from app.services.transcription import transcribe_audio


router = APIRouter(tags=["legacy"])
validator = RequestValidator(settings.TWILIO_TOKEN)
DEPRECATION_MSG = "Deprecated endpoint; migrate to /v1/* routes"


def validation_error_response(message: str, request: Request, exc: ValidationError) -> JSONResponse:
    envelope = ErrorEnvelope(
        error=ErrorPayload(
            code="validation_error",
            message=message,
            trace_id=request.headers.get("X-Trace-Id"),
            retryable=False,
            details={"errors": exc.errors()},
        )
    )
    return JSONResponse(content=envelope.model_dump(), status_code=400)


async def validate_twilio_request(request: Request) -> dict:
    signature = request.headers.get("X-Twilio-Signature")
    form = await request.form()
    data = dict(form)
    if data.get("AccountSid") != settings.TWILIO_SID:
        raise HTTPException(status_code=401, detail="Invalid Twilio account")
    if not signature or not validator.validate(str(request.url), data, signature):
        raise HTTPException(status_code=401, detail="Invalid Twilio signature")
    return data


@router.post("/process-call")
def process_call(payload: dict, request: Request, _: None = Depends(require_voice_token)) -> Response:
    try:
        data = VoiceRequest.model_validate(payload)
    except ValidationError as exc:
        return validation_error_response("Invalid voice payload", request, exc)

    twiml = build_initial_twiml(data.model_dump())
    return Response(
        content=twiml,
        media_type="text/xml",
        headers={"Warning": f'299 - "{DEPRECATION_MSG}"'},
    )


@router.post("/transcribe")
async def transcribe(request: Request) -> Response:
    form = await validate_twilio_request(request)
    audio = form.get("audio")
    text = form.get("SpeechResult") or ""
    if audio is not None:
        data = await audio.read() if hasattr(audio, "read") else audio
        text = transcribe_audio(data)

    twiml = build_transcribe_twiml({"speech_result": text})

    return Response(
        content=twiml,
        media_type="application/xml",
        headers={"Warning": f'299 - "{DEPRECATION_MSG}"'},
    )


@router.post("/partial")
async def partial(request: Request) -> JSONResponse:
    await validate_twilio_request(request)
    return JSONResponse({"ok": True}, headers={"Warning": f'299 - "{DEPRECATION_MSG}"'})
