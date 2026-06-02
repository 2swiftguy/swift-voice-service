import logging

from redis.exceptions import RedisError

from app.core.deps import redis_client

logger = logging.getLogger(__name__)


def get_state(sid: str) -> dict:
    if not sid:
        return {}
    try:
        return redis_client.hgetall(f"call:{sid}")
    except RedisError as exc:  # pragma: no cover - depends on runtime redis
        logger.warning("call_state_redis_unavailable", extra={"error": str(exc)})
        return {}


def set_state(sid: str, **kv):
    if sid:
        try:
            redis_client.hset(f"call:{sid}", mapping=kv)
            redis_client.expire(f"call:{sid}", 3600)
        except RedisError as exc:  # pragma: no cover - depends on runtime redis
            logger.warning("call_state_redis_unavailable", extra={"error": str(exc)})
