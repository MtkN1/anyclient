from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from anyfetch._models import (
    AsyncHTTPClient,
    AsyncWebSocketClient,
    AsyncWebSocketConnection,
    Response,
)

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    import aiohttp

    from anyfetch._models import (
        Request,
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
            if response.version is None:
                http_version = ""
            else:
                major, minor = response.version
                http_version = f"{major}.{minor}"

            return Response(
                http_version=http_version,
                status_code=response.status,
                reason_phrase=response.reason or "",
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
        await self._websocket.send_bytes(data) if isinstance(
            data, bytes
        ) else await self._websocket.send_str(data)

    async def receive(self) -> str | bytes:
        msg = await self._websocket.receive()
        if isinstance(msg.data, str | bytes):
            return msg.data

        raise ValueError
