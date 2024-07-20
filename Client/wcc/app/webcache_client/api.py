import os
from typing import Any, Type, TypeVar

import httpx
from app.lib.http_method import HTTP_METHOD  # type: ignore
from httpx import Request, Response
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


class WebCacheException(Exception):
    pass


class WebCacheApi:
    def __init__(self) -> None:
        self.gateway = os.environ.get(
            "WEBCACHE_URL", "http://localhost:8888/webcache"
        )

    def _build_url(self, path: str) -> str:
        return f"{self.gateway}/{path}"

    def _build_request(
        self,
        method: HTTP_METHOD,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        path: str | None = None,
    ) -> Request:
        url = self.gateway if path is None else self._build_url(path)
        return Request(method=method, params=params, url=str(url), json=json)

    async def _send(self, request: Request) -> Response:
        c = httpx.AsyncClient()
        resp = await c.send(request)
        return resp

    async def result(
        self,
        method: HTTP_METHOD,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        path: str | None = None,
    ) -> Response:
        req = self._build_request(
            method=method, json=json, params=params, path=path
        )
        resp = await self._send(req)
        if resp.text != "OK":
            print("response not OK")
            raise WebCacheException()
        return resp

    async def model_result(
        self,
        model: Type[T],
        method: HTTP_METHOD,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        path: str | None = None,
    ) -> T:
        req = self._build_request(
            method=method, json=json, params=params, path=path
        )
        resp = await self._send(req)
        try:
            return model(**resp.json())
        except ValidationError:
            print(resp.content)
            print(resp.text)
            raise WebCacheException()
