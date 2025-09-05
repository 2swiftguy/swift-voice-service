from fastapi import FastAPI
from app.core.logging import setup_logging
from app.middleware.request_id import RequestIdMiddleware
from app.routes.http import router as http_router
from app.routes.sms_handler import router as sms_router

setup_logging()
app = FastAPI(title="SWIFT Voice Service — Barge-In Ready")
app.add_middleware(RequestIdMiddleware)
app.include_router(http_router)
app.include_router(sms_router)
