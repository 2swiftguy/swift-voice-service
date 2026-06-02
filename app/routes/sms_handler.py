from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.core.auth import require_sms_token
from app.models.contracts import ErrorEnvelope, ErrorPayload, SmsRequest
from app.services.sms_handler import build_sms_response

router = APIRouter(tags=["legacy"])
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


@router.post("/process-sms")
def process_sms(payload: dict, request: Request, _: None = Depends(require_sms_token)) -> Response:
    try:
        data = SmsRequest.model_validate(payload)
    except ValidationError as exc:
        return validation_error_response("Invalid SMS payload", request, exc)

    twiml_response = build_sms_response(f"Received {data.message_sid}")
    return Response(content=twiml_response, media_type="text/xml")


@router.post("/sms")
def sms_handler(_: None = Depends(require_sms_token)) -> Response:
    twiml_response = build_sms_response("Hello from Swift!")
    return Response(
        content=twiml_response,
        media_type="text/xml",
        headers={"Warning": f'299 - "{DEPRECATION_MSG}"'},
    )
