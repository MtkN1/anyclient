from __future__ import annotations

from typing import TYPE_CHECKING

from anyfetch._models import HTTPClient

if TYPE_CHECKING:
    import urllib3

    from anyfetch._models import Request, Response


class Urllib3Client(HTTPClient):
    def __init__(self, pool: urllib3.PoolManager) -> None:
        self._pool = pool

    def request(self, request: Request) -> Response:
        raise NotImplementedError
