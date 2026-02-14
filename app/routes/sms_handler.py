from fastapi import APIRouter, Header, HTTPException, Response

from app.core.settings import settings

router = APIRouter(tags=["legacy"])
DEPRECATION_MSG = "Deprecated endpoint; migrate to /v1/* routes"


@router.post("/sms")
def sms_handler(x_service_token: str | None = Header(None)) -> Response:
    if x_service_token != settings.PYTHON_SMS_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    twiml_response = "<Response><Message>Hello from Swift!</Message></Response>"
    return Response(
        content=twiml_response,
        media_type="application/xml",
        headers={"Warning": f'299 - "{DEPRECATION_MSG}"'},
    )
