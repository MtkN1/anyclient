from __future__ import annotations

from contextlib import asynccontextmanager, contextmanager
from typing import TYPE_CHECKING

from anyfetch._models import (
    AsyncHTTPClient,
    AsyncWebSocketClient,
    AsyncWebSocketConnection,
    HTTPClient,
    Request,
    Response,
    WebSocketClient,
    WebSocketConnection,
)

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Generator

    import httpx
    import httpx_ws


class HttpxClient(HTTPClient):
    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def request(self, request: Request) -> Response:
        raise NotImplementedError


class HttpxWebSocketClient(WebSocketClient):
    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    @contextmanager
    def connect(self, url: str) -> Generator[WebSocketConnection]:
        raise NotImplementedError


class HttpxWebSocketConnection(WebSocketConnection):
    def __init__(self, session: httpx_ws.WebSocketSession) -> None:
        self._session = session

    def send(self, data: str | bytes) -> None:
        raise NotImplementedError

    def receive(self) -> str | bytes:
        raise NotImplementedError


class AsyncHttpxClient(AsyncHTTPClient):
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def request(self, request: Request) -> Response:
        raise NotImplementedError


class AsyncHttpxWebSocketClient(AsyncWebSocketClient):
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    @asynccontextmanager
    async def connect(self, url: str) -> AsyncGenerator[AsyncHttpxWebSocketConnection]:
        raise NotImplementedError


class AsyncHttpxWebSocketConnection(AsyncWebSocketConnection):
    def __init__(self, session: httpx_ws.AsyncWebSocketSession) -> None:
        self._session = session

    async def send(self, data: str | bytes) -> None:
        raise NotImplementedError

    async def receive(self) -> str | bytes:
        raise NotImplementedError
