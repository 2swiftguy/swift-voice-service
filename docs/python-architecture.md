# Python Service Architecture Review

## Current state
- The service currently mixes public API routes with Twilio webhook compatibility routes in the same app process.
- Business logic for transcription/call flow exists in service modules, but route boundaries and schemas are inconsistent.
- Redis is already used for call state; this is aligned with stateless worker expectations when paired with TTL.
- Request correlation existed via `X-Request-ID`; this has been standardized to `trace_id` (`X-Trace-Id`) and JSON logs.

## Risks observed
- Public API surface was broad and ambiguous (`/process-call`, `/sms`, `/transcribe`, `/partial` exposed beside health endpoints).
- Request/response contracts were not fully versioned or consistently typed with explicit schemas.
- Long-running AI operations can block workers if no timeout/retry policy is enforced.
- Deprecated compatibility routes may continue being used unless migration path is explicit.

## Target shape
- Public API surface (v1):
  - `POST /v1/transcribe`
  - `POST /v1/classify-intent`
  - `POST /v1/generate-reply`
  - `GET /health`
  - `GET /ready`
  - Streaming routes: `POST /v1/streaming/sessions`, `POST /v1/streaming/partial`
- Legacy routes remain for compatibility, but return deprecation warnings so clients can migrate safely.
- All JSON request and response bodies are represented by strict Pydantic v1 models (`*V1` types).
- Service remains stateless:
  - No persistent in-memory state.
  - Streaming metadata is stored in Redis with TTL.
- AI worker tasks apply safe timeout + retry defaults (`WORKER_TIMEOUT_SECONDS`, bounded retries).

## Async/queued guidance for long-running work
- Current AI worker actions are asynchronous and bounded via timeout/retry.
- If transcription/classification latency exceeds request SLAs, move execution to a queue-based worker (e.g., Celery/RQ) and expose job-based APIs:
  - `POST /v1/jobs/*` to enqueue.
  - `GET /v1/jobs/{id}` to poll status/results.
- Keep request handlers lightweight and return quickly under load.
