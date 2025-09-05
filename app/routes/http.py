from fastapi import APIRouter, Header, HTTPException, Request
from fastapi.responses import Response, JSONResponse
from app.core.settings import settings
from app.models.call import CallPayload
from app.services.call_flow import build_initial_twiml, build_transcribe_twiml
from app.services.transcription import transcribe_audio

router = APIRouter()

@router.get("/health")
def health(): return {"ok": True}

@router.get("/ready")
def ready(): return {"ok": True}

@router.post("/process-call")
def process_call(payload: CallPayload, x_service_token: str | None = Header(None)):
    if x_service_token != settings.SERVICE_AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    twiml = build_initial_twiml(payload.dict())
    return Response(content=twiml, media_type="application/xml")

@router.post("/transcribe")
async def transcribe(request: Request):
    form = await request.form()

    # Prefer transcribing any uploaded audio ourselves using an in-memory buffer
    # rather than persisting to a temporary file on disk.
    audio = form.get("audio")
    text = form.get("SpeechResult") or ""
    if audio is not None:
        data = await audio.read() if hasattr(audio, "read") else audio
        text = transcribe_audio(data)

    twiml = build_transcribe_twiml({"SpeechResult": text})
    return Response(content=twiml, media_type="application/xml")

@router.post("/partial")
async def partial(request: Request):
    # Receives partial ASR results from Twilio if PUBLIC_BASE_URL is set
    data = await request.form()
    return JSONResponse({"ok": True})