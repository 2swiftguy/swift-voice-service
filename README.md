# SWIFT Python Service — Barge‑in Ready

Twilio `<Gather input="speech dtmf" bargeIn="true">` with optional partial ASR callbacks.

## Quick start
```bash
docker compose up -d
docker compose logs -f swift-python-service
curl http://127.0.0.1:8001/health
```

Create `.env.local` before starting the container:
```dotenv
TWILIO_SID=your-twilio-account-sid
TWILIO_TOKEN=your-twilio-auth-token
PYTHON_VOICE_TOKEN=shared-voice-secret
PYTHON_SMS_TOKEN=shared-sms-secret
```

## Laravel integration
The `2swiftguy/haroldhowell` app posts JSON to:

- `POST /process-call` with `from`, `to`, `call_sid`, and `trace_id`
- `POST /process-sms` with `from`, `to`, `body`, `message_sid`, and `trace_id`

Both endpoints require `X-Service-Token` and echo request correlation with `X-Trace-Id`.
