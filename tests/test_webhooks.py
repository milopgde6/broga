import socket

import aiohttp
import pytest

from app.payments import webhooks


@pytest.mark.asyncio
async def test_health_endpoint_uses_render_port(monkeypatch):
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]

    monkeypatch.setattr(webhooks, "WEBHOOK_HOST", "127.0.0.1")
    monkeypatch.setenv("PORT", str(port))
    runner = await webhooks.start_webhook_server()
    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(f"http://127.0.0.1:{port}/health") as response:
                assert response.status == 200
                assert await response.json() == {"ok": True}
            async with client.get(f"http://127.0.0.1:{port}/") as response:
                assert response.status == 200
                assert (await response.json())["ok"] is True
    finally:
        await runner.cleanup()
