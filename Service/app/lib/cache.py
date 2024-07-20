import base64
import gzip
import os
from typing import Any, Type, TypeVar

from pydantic import BaseModel

"""
A cache class to save information to disk.
Uses the given cache_model to return the cache as that model.
Compresses and b64 encodes the cache for compression purposes.

TODO:
add redis support to use memory rather than disk
"""

T = TypeVar("T", bound=BaseModel)


class Cache:
    def __init__(
        self,
        cache_file_path: str,
        cache_model: Type[T],
    ) -> None:
        self.cache_file_path: str = f"{cache_file_path}.cache"
        self.cache_model: Type[T] = cache_model

    def _compress_data(self, data: str, compressor: Any) -> bytes:
        compressed_data = compressor.compress(data.encode("utf-8"))
        return base64.b64encode(compressed_data)

    def _decompress_data(self, data: bytes, decompressor: Any) -> str:
        decompressed_data = decompressor.decompress(base64.b64decode(data))
        return decompressed_data.decode("utf-8")

    def save_cache(self, cache: T) -> None:
        if not isinstance(cache, self.cache_model):
            raise ValueError("Invalid cache model given")

        cache_as_json = cache.model_dump_json()
        compressed_data = self._compress_data(cache_as_json, gzip)

        with open(self.cache_file_path, "wb") as f:
            f.write(compressed_data)
            f.flush()

    def load_cache(self) -> T | None:
        if not os.path.exists(self.cache_file_path):
            return None

        with open(self.cache_file_path, "rb") as f:
            compressed_data = f.read()

        decompressed_data = self._decompress_data(
            compressed_data, decompressor=gzip
        )  # noqa: E501
        try:
            return self.cache_model.model_validate_json(decompressed_data)  # type: ignore # noqa: E501
        except Exception:
            return None
