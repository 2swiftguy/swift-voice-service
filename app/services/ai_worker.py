import asyncio
import logging
from dataclasses import dataclass

from app.core.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class RetryPolicy:
    attempts: int = 2
    backoff_seconds: float = 0.15


async def _with_retry(coro_factory, policy: RetryPolicy):
    last_error = None
    for attempt in range(1, policy.attempts + 1):
        try:
            return await coro_factory()
        except Exception as exc:  # pragma: no cover - covered by integration behavior
            last_error = exc
            logger.warning("worker_attempt_failed", extra={"attempt": attempt, "error": str(exc)})
            if attempt < policy.attempts:
                await asyncio.sleep(policy.backoff_seconds * attempt)
    raise last_error


async def classify_intent(text: str) -> tuple[str, float]:
    async def _classify():
        lowered = text.lower()
        if any(word in lowered for word in ["help", "support", "issue"]):
            return "support", 0.92
        if any(word in lowered for word in ["buy", "price", "quote"]):
            return "sales", 0.87
        return "general", 0.74

    timeout = settings.WORKER_TIMEOUT_SECONDS
    return await asyncio.wait_for(_with_retry(_classify, RetryPolicy()), timeout=timeout)


async def generate_reply(text: str, intent: str | None) -> str:
    async def _reply():
        inferred_intent = intent or (await classify_intent(text))[0]
        templates = {
            "support": "I can help with that support issue. Could you share your account email?",
            "sales": "Happy to help with pricing. What plan size are you considering?",
            "general": "Thanks for your message. Could you share a little more detail?",
        }
        return templates.get(inferred_intent, templates["general"])

    timeout = settings.WORKER_TIMEOUT_SECONDS
    return await asyncio.wait_for(_with_retry(_reply, RetryPolicy()), timeout=timeout)
