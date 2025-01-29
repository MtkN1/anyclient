from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from anyfetch._models import (
    AsyncHTTPClient,
    AsyncWebSocketClient,
    AsyncWebSocketConnection,
)

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    import aiohttp

    from anyfetch._models import (
        Request,
        Response,
    )


class AiohttpClient(AsyncHTTPClient):
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self._session = session

    async def request(self, request: Request) -> Response:
        async with self._session.request(
            method=request.method,
            url=request.url,
            headers=request.headers,
            data=request.content,
        ) as response:
            return Response(
                http_version=response.version,
                status_code=response.status,
                reason_phrase=response.reason,
                headers=dict(response.headers),
                content=await response.read(),
            )


class AiohttpWebSocketClient(AsyncWebSocketClient):
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self._session = session

    @asynccontextmanager
    async def connect(self, url: str) -> AsyncGenerator[AiohttpWebSocketConnection]:
        async with self._session.ws_connect(url) as websocket:
            yield AiohttpWebSocketConnection(websocket)


class AiohttpWebSocketConnection(AsyncWebSocketConnection):
    def __init__(self, websocket: aiohttp.ClientWebSocketResponse) -> None:
        self._websocket = websocket

    async def send(self, data: str | bytes) -> None:
        await self._websocket.send_bytes(data) if isinstance(data, bytes) else await self._websocket.send_str(data)

    async def receive(self) -> str | bytes:
        msg = await self._websocket.receive()
        return msg.data if msg.type == aiohttp.WSMsgType.TEXT else msg.data
