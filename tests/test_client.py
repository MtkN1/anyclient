"""Test client module."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import aiohttp
import httpx
import pytest
import urllib3

import anyfetch

if TYPE_CHECKING:
    from collections.abc import Callable
    from contextlib import AbstractAsyncContextManager, AbstractContextManager


@dataclass
class _InputSyncHTTPClient:
    client_cls: type[anyfetch.HTTPClient]
    base_cls_factory: Callable[..., AbstractContextManager[object]]


@pytest.mark.parametrize(
    "test_input",
    [
        _InputSyncHTTPClient(anyfetch.HttpxClient, httpx.Client),
        _InputSyncHTTPClient(anyfetch.Urllib3Client, urllib3.PoolManager),
    ],
)
def test_sync_client(test_input: _InputSyncHTTPClient) -> None:
    """Test for sync client."""
    with test_input.base_cls_factory() as adapter:
        client = test_input.client_cls(adapter)

        request = anyfetch.Request("GET", "https://httpbin.org/get")
        response = client.request(request)

    assert response.status_code == 200


@dataclass
class _InputSyncWebSocketClient:
    client_cls: type[anyfetch.WebSocketClient]
    base_cls_factory: Callable[..., AbstractContextManager[object]]


@pytest.mark.parametrize(
    "test_input",
    [
        _InputSyncWebSocketClient(anyfetch.HttpxWebSocketClient, httpx.Client),
    ],
)
def test_sync_websocket_client(test_input: _InputSyncWebSocketClient) -> None:
    """Test for sync client."""
    with test_input.base_cls_factory() as adapter:
        client = test_input.client_cls(adapter)

        url = "wss://echo.websocket.org"
        with client.connect(url) as websocket:
            websocket.send("Hello, World!")
            websocket.receive()


@dataclass
class _InputAsyncHTTPClient:
    client_cls: type[anyfetch.AsyncHTTPClient]
    base_cls_factory: Callable[..., AbstractAsyncContextManager[object]]


@pytest.mark.parametrize(
    ("test_input", "anyio_backend"),
    [
        (
            _InputAsyncHTTPClient(anyfetch.AsyncHttpxClient, httpx.AsyncClient),
            "asyncio",
        ),
        (
            _InputAsyncHTTPClient(anyfetch.AsyncHttpxClient, httpx.AsyncClient),
            "trio",
        ),
        (
            _InputAsyncHTTPClient(anyfetch.AiohttpClient, aiohttp.ClientSession),
            "asyncio",
        ),
    ],
)
async def test_async_client(
    test_input: _InputAsyncHTTPClient, anyio_backend: str
) -> None:
    """Test for asyncio client."""
    async with test_input.base_cls_factory() as adapter:
        client = test_input.client_cls(adapter)

        request = anyfetch.Request("GET", "https://httpbin.org/get")
        response = await client.request(request)

    assert response.status_code == 200


@dataclass
class _InputAsyncWebSocketClient:
    client_cls: type[anyfetch.AsyncWebSocketClient]
    base_cls_factory: Callable[..., AbstractAsyncContextManager[object]]


@pytest.mark.parametrize(
    ("test_input", "anyio_backend"),
    [
        (
            _InputAsyncWebSocketClient(
                anyfetch.AsyncHttpxWebSocketClient, httpx.AsyncClient
            ),
            "asyncio",
        ),
        (
            _InputAsyncWebSocketClient(
                anyfetch.AsyncHttpxWebSocketClient, httpx.AsyncClient
            ),
            "trio",
        ),
        (
            _InputAsyncWebSocketClient(
                anyfetch.AiohttpWebSocketClient, aiohttp.ClientSession
            ),
            "asyncio",
        ),
    ],
)
async def test_async_websocket_client(
    test_input: _InputAsyncWebSocketClient, anyio_backend: str
) -> None:
    """Test for sync client."""
    async with test_input.base_cls_factory() as adapter:
        client = test_input.client_cls(adapter)

        url = "wss://echo.websocket.org"
        async with client.connect(url) as websocket:
            await websocket.send("Hello, World!")
            await websocket.receive()
