from fastapi import FastAPI

from app.core.logging import setup_logging
from app.middleware.request_id import RequestIdMiddleware
from app.routes.http import router as legacy_http_router
from app.routes.sms_handler import router as legacy_sms_router
from app.routes.v1 import public_router, router as v1_router

setup_logging()
app = FastAPI(title="SWIFT Python Service — Stateless AI Worker")
app.add_middleware(RequestIdMiddleware)
app.include_router(public_router)
app.include_router(v1_router)
app.include_router(legacy_http_router)
app.include_router(legacy_sms_router)
