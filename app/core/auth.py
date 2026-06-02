from secrets import compare_digest

from fastapi import Header, HTTPException

from app.core.settings import settings


def service_token_matches(provided_token: str | None, expected_token: str) -> bool:
    if provided_token is None:
        return False
    return compare_digest(provided_token, expected_token)


def _require_service_token(provided_token: str | None, expected_token: str) -> None:
    if not service_token_matches(provided_token, expected_token):
        raise HTTPException(status_code=401, detail="Unauthorized")


def require_voice_token(x_service_token: str | None = Header(None)) -> None:
    _require_service_token(x_service_token, settings.PYTHON_VOICE_TOKEN)


def require_sms_token(x_service_token: str | None = Header(None)) -> None:
    _require_service_token(x_service_token, settings.PYTHON_SMS_TOKEN)
