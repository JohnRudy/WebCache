import asyncio
import getpass

from app.lib.file_operations import (  # type: ignore
    get_file_schema,
    place_content_into_file
)
from app.webcache_client.api import WebCacheApi  # type: ignore
from app.webcache_client.schema import (  # type: ignore
    File,
    WebCache,
    WebCacheKeys
)


class WebCacheClient:
    def __init__(self) -> None:
        self.CACHE_KEY: str = getpass.getuser()
        self.api = WebCacheApi()

    def _is_key_present(self, key: str) -> bool:
        req = self.api._build_request("GET", params={"key": key})
        resp = asyncio.run(self.api._send(req))
        if resp.text == "NA":
            return False
        return True

    def remove_key(self, key: str, exact: bool = False) -> None:
        if not exact:
            key = f"{self.CACHE_KEY}{key}"
        if not self._is_key_present(key):
            print("Key is not present in cache")
            return
        asyncio.run(self.api.result("DELETE", params={"key": key}))

    def get_keys(self, all: bool = False) -> list[str]:
        resp = asyncio.run(
            self.api.model_result(method="GET", model=WebCacheKeys, path="keys")
        )
        if not all:
            return [
                x.replace(self.CACHE_KEY, "")
                for x in resp.keys
                if self.CACHE_KEY in x
            ]
        else:
            return resp.keys

    def cache_item(
        self,
        filepath: str | None = None,
        key: str | None = None,
        value: str | None = None,
        force: bool = False,
        exact: bool = False,
    ) -> None:
        if filepath:
            f = get_file_schema(filepath)
            if not exact:
                key = f"{self.CACHE_KEY}{f.name}"
            if self._is_key_present(str(key)) and not force:
                print("Key is present in cache, use '--force' to override")
                return
            wc = WebCache(key=key, value=f.content)
        elif key and value:
            if not exact:
                key = f"{self.CACHE_KEY}{key}"
            if self._is_key_present(key) and not force:
                print("Key is present in cache, use '--force' to override")
                return
            wc = WebCache(key=key, value=value)
        else:
            print(
                f"Missing parameters FILEPATH: {filepath}, KEY: {key}, VALUE: {value}"  # noqa: E501
            )
            return
        asyncio.run(self.api.result("POST", json=wc.model_dump()))

    def fetch_item(
        self,
        filename: str | None = None,
        key: str | None = None,
        exact: bool = False,
    ) -> str | None:
        if filename:
            if not exact:
                key = f"{self.CACHE_KEY}{filename}"
            else:
                key = filename
            if not self._is_key_present(key):
                print("Key is not present in cache")
                return None
        elif key:
            if not exact:
                key = f"{self.CACHE_KEY}{key}"
            if not self._is_key_present(key):
                print("Key is not present in cache")
                return None
        else:
            print(f"Missing parameters FILEPATH: {filename}, KEY: {key}")
            return None

        wc = asyncio.run(
            self.api.model_result(
                model=WebCache, method="GET", params={"key": key}
            )
        )
        if filename:
            f = File(name=filename, content=wc.value)
            place_content_into_file(f)
            return_value = f.name
        else:
            return_value = wc.value

        return return_value
