
import contextvars

import logging
import uuid

from starlette.middleware.base import BaseHTTPMiddleware




# Context variable to store the current request ID
_request_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="")


class RequestIdFilter(logging.Filter):
    """Logging filter that injects the current request ID into log records."""

    def filter(self, record: logging.LogRecord) -> bool:  # pragma: no cover - trivial
        record.request_id = _request_id_ctx.get()
        return True


# Attach the filter once to the root logger
_root_logger = logging.getLogger()
if not any(isinstance(f, RequestIdFilter) for f in _root_logger.filters):
    _root_logger.addFilter(RequestIdFilter())



class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        rid = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        token = _request_id_ctx.set(rid)
        try:
            resp = await call_next(request)
        finally:
            _request_id_ctx.reset(token)
        resp.headers["X-Request-ID"] = rid
        return resp

