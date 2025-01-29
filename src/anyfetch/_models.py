from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Protocol

if sys.version_info >= (3, 11):
    from typing import dataclass_transform
else:
    from typing_extensions import dataclass_transform

if TYPE_CHECKING:
    from collections.abc import Coroutine, Mapping
    from contextlib import AbstractAsyncContextManager, AbstractContextManager

    from _typeshed import DataclassInstance


@dataclass_transform(
    eq_default=True,
    kw_only_default=True,
    frozen_default=True,
    field_specifiers=(field,),
)
def json_object(cls: type[DataclassInstance]) -> type[DataclassInstance]:
    if sys.version_info >= (3, 11):
        wrap = dataclass(
            eq=True, frozen=True, kw_only=True, slots=True, weakref_slot=True
        )
    else:
        wrap = dataclass(eq=True, frozen=True, kw_only=True, slots=True)

    return wrap(cls)


@dataclass_transform(
    eq_default=True,
    frozen_default=True,
    field_specifiers=(field,),
)
def dataclass_base(cls: type[DataclassInstance]) -> type[DataclassInstance]:
    if sys.version_info >= (3, 11):
        wrap = dataclass(
            eq=True, frozen=True, kw_only=True, slots=True, weakref_slot=True
        )
    else:
        wrap = dataclass(eq=True, frozen=True, slots=True)

    return wrap(cls)


@dataclass_base
class Request:
    method: str
    url: str
    headers: Mapping[str, str] = field(default_factory=dict, kw_only=True)
    content: bytes = field(default=b"", kw_only=True)


@dataclass_base
class Response:
    http_version: str
    status_code: int
    reason_phrase: str
    headers: Mapping[str, str] = field(default_factory=dict, kw_only=True)
    content: bytes = field(default=b"", kw_only=True)


class HTTPClient(Protocol):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

    def request(self, request: Request) -> Response: ...


class AsyncHTTPClient(Protocol):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

    def request(self, request: Request) -> Coroutine[Any, Any, Response]: ...


class WebSocketClient(Protocol):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

    def connect(self, url: str) -> AbstractContextManager[WebSocketConnection]: ...


class WebSocketConnection(Protocol):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

    def send(self, data: str | bytes) -> None: ...
    def receive(self) -> str | bytes: ...


class AsyncWebSocketClient(Protocol):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

    def connect(
        self, url: str
    ) -> AbstractAsyncContextManager[AsyncWebSocketConnection]: ...


class AsyncWebSocketConnection(Protocol):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

    def send(self, data: str | bytes) -> Coroutine[Any, Any, None]: ...
    def receive(self) -> Coroutine[Any, Any, str | bytes]: ...
