from fastapi import APIRouter, Response, Header, HTTPException

from app.core.settings import settings

router = APIRouter()

@router.post("/sms")
def sms_handler(x_service_token: str | None = Header(None)) -> Response:
    """Handle incoming SMS webhooks from Twilio."""
    if x_service_token != settings.SERVICE_AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    twiml_response = "<Response><Message>Hello from Swift!</Message></Response>"
    return Response(content=twiml_response, media_type="application/xml")

