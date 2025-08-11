from starlette.middleware.base import BaseHTTPMiddleware
import uuid, logging
class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        rid = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        for h in logging.getLogger().handlers:
            h.addFilter(lambda rec: setattr(rec, "request_id", rid) or True)
        resp = await call_next(request)
        resp.headers["X-Request-ID"] = rid
        return resp