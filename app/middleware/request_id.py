import contextvars
import logging
import uuid

from starlette.middleware.base import BaseHTTPMiddleware


trace_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("trace_id", default="")


class TraceIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:  # pragma: no cover - trivial
        record.trace_id = trace_id_ctx.get()
        return True


_root_logger = logging.getLogger()
if not any(isinstance(f, TraceIdFilter) for f in _root_logger.filters):
    _root_logger.addFilter(TraceIdFilter())


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        trace_id = request.headers.get("X-Trace-Id") or str(uuid.uuid4())
        request.state.trace_id = trace_id
        token = trace_id_ctx.set(trace_id)
        try:
            response = await call_next(request)
        finally:
            trace_id_ctx.reset(token)
        response.headers["X-Trace-Id"] = trace_id
        return response
