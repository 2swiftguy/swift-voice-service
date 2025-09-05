import base64
from typing import Iterable
from fastapi import WebSocket


async def synthesize_and_stream_audio(stream: Iterable[bytes], websocket: WebSocket) -> None:
    """Stream base64 encoded audio chunks to a websocket sequentially."""
    for chunk in stream:
        b64_chunk = base64.b64encode(chunk).decode("ascii")
        await websocket.send_text(b64_chunk)


async def handle_stream_session(stream: Iterable[bytes], websocket: WebSocket) -> None:
    """swift-python-service WebSocket session handler."""
    await synthesize_and_stream_audio(stream, websocket)
