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
        raise NotImplementedError


class AiohttpWebSocketClient(AsyncWebSocketClient):
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self._session = session

    @asynccontextmanager
    async def connect(self, url: str) -> AsyncGenerator[AiohttpWebSocketConnection]:
        raise NotImplementedError


class AiohttpWebSocketConnection(AsyncWebSocketConnection):
    def __init__(self, websocket: aiohttp.ClientWebSocketResponse) -> None:
        self._websocket = websocket

    async def send(self, data: str | bytes) -> None:
        raise NotImplementedError

    async def receive(self) -> str | bytes:
        raise NotImplementedError
