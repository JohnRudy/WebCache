from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse, PlainTextResponse

from app.lib.webcache import get_webcache
from app.schemas.schemas import ItemSchema

router = APIRouter()

wc = get_webcache()


@router.post("/")
def new_cache_item(item: ItemSchema) -> PlainTextResponse:
    wc.add_cache_item(item.key, item.value)
    return PlainTextResponse("OK")


@router.get("/")
def get_cache_item(key: str) -> Any:
    item = wc.get_cache_item(key)
    if item:
        return ItemSchema(key=key, value=item)
    else:
        return PlainTextResponse("NA")


@router.delete("/")
def remove_cache_item(key: str) -> PlainTextResponse:
    txt = wc.remove_item(key)
    return PlainTextResponse(txt)


@router.get("/keys")
def get_webcache_keys() -> JSONResponse:
    keys = wc.get_cache_keys()
    return JSONResponse(content={"keys": keys})
