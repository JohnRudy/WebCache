from typing import Any

from pydantic import BaseModel


class RootCache(BaseModel):
    cache: dict[str, Any] = {}


class ItemSchema(BaseModel):
    key: str
    value: Any
