# SWIFT Voice Service — Barge‑in Ready

Twilio `<Gather input="speech dtmf" bargeIn="true">` with optional partial ASR callbacks.

## Quick start
```bash
cp .env.local.example .env.local.local
docker compose up -d
docker compose logs -f voice
curl http://127.0.0.1:8001/health
```