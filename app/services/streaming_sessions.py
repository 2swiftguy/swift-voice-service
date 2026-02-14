import logging
import uuid

from redis.exceptions import RedisError

from app.core.deps import redis_client
from app.core.settings import settings

logger = logging.getLogger(__name__)


def create_streaming_session(call_sid: str, stage: str) -> tuple[str, int]:
    session_id = str(uuid.uuid4())
    key = f"stream:{session_id}"
    ttl_seconds = settings.STREAMING_SESSION_TTL_SECONDS
    payload = {"call_sid": call_sid, "stage": stage}
    try:
        redis_client.hset(key, mapping=payload)
        redis_client.expire(key, ttl_seconds)
    except RedisError as exc:  # pragma: no cover - depends on runtime redis
        logger.warning("stream_session_redis_unavailable", extra={"error": str(exc)})
    return session_id, ttl_seconds


def update_partial(session_id: str, partial_text: str) -> None:
    key = f"stream:{session_id}"
    ttl_seconds = settings.STREAMING_SESSION_TTL_SECONDS
    try:
        redis_client.hset(key, mapping={"last_partial": partial_text})
        redis_client.expire(key, ttl_seconds)
    except RedisError as exc:  # pragma: no cover
        logger.warning("stream_partial_redis_unavailable", extra={"error": str(exc)})
