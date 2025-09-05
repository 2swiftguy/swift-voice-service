from fastapi import APIRouter, Response

router = APIRouter()

@router.post("/sms")
def sms_handler() -> Response:
    """Handle incoming SMS webhooks from Twilio."""
    twiml_response = "<Response><Message>Hello from Swift!</Message></Response>"
    return Response(content=twiml_response, media_type="application/xml")

