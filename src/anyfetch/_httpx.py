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
        response = self._client.request(
            method=request.method,
            url=request.url,
            headers=request.headers,
            content=request.content,
        )
        return Response(
            http_version=response.http_version,
            status_code=response.status_code,
            reason_phrase=response.reason_phrase,
            headers=dict(response.headers),
            content=response.content,
        )


class HttpxWebSocketClient(WebSocketClient):
    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    @contextmanager
    def connect(self, url: str) -> Generator[HttpxWebSocketConnection]:
        with self._client.ws_connect(url) as websocket:
            yield HttpxWebSocketConnection(websocket)


class HttpxWebSocketConnection(WebSocketConnection):
    def __init__(self, session: httpx_ws.WebSocketSession) -> None:
        self._session = session

    def send(self, data: str | bytes) -> None:
        if isinstance(data, bytes):
            self._session.send_bytes(data)
        else:
            self._session.send_str(data)

    def receive(self) -> str | bytes:
        msg = self._session.receive()
        return msg.data if msg.type == httpx_ws.WSMsgType.TEXT else msg.data


class AsyncHttpxClient(AsyncHTTPClient):
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def request(self, request: Request) -> Response:
        response = await self._client.request(
            method=request.method,
            url=request.url,
            headers=request.headers,
            content=request.content,
        )
        return Response(
            http_version=response.http_version,
            status_code=response.status_code,
            reason_phrase=response.reason_phrase,
            headers=dict(response.headers),
            content=response.content,
        )


class AsyncHttpxWebSocketClient(AsyncWebSocketClient):
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    @asynccontextmanager
    async def connect(self, url: str) -> AsyncGenerator[AsyncHttpxWebSocketConnection]:
        async with self._client.ws_connect(url) as websocket:
            yield AsyncHttpxWebSocketConnection(websocket)


class AsyncHttpxWebSocketConnection(AsyncWebSocketConnection):
    def __init__(self, session: httpx_ws.AsyncWebSocketSession) -> None:
        self._session = session

    async def send(self, data: str | bytes) -> None:
        if isinstance(data, bytes):
            await self._session.send_bytes(data)
        else:
            await self._session.send_str(data)

    async def receive(self) -> str | bytes:
        msg = await self._session.receive()
        return msg.data if msg.type == httpx_ws.WSMsgType.TEXT else msg.data
