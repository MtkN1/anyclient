from __future__ import annotations

from typing import TYPE_CHECKING

from anyfetch._models import HTTPClient, Response

if TYPE_CHECKING:
    import urllib3

    from anyfetch._models import Request


class Urllib3Client(HTTPClient):
    def __init__(self, pool: urllib3.PoolManager) -> None:
        self._pool = pool

    def request(self, request: Request) -> Response:
        response = self._pool.request(
            method=request.method,
            url=request.url,
            headers=request.headers,
            body=request.content,
        )
        return Response(
            http_version="1.1",
            status_code=response.status,
            reason_phrase=response.reason,
            headers=dict(response.headers),
            content=response.data,
        )
