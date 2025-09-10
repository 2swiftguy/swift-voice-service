from app.core.deps import redis_client


def get_state(sid: str) -> dict:
    return redis_client.hgetall(f"call:{sid}") if sid else {}


def set_state(sid: str, **kv):
    if sid:
        redis_client.hset(f"call:{sid}", mapping=kv)
        redis_client.expire(f"call:{sid}", 3600)
