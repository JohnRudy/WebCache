from pydantic import BaseModel


class WebCache(BaseModel):
    key: str
    value: str


class WebCacheKeys(BaseModel):
    keys: list[str]


class File(BaseModel):
    name: str
    content: str
