import os

from app.webcache_client.wcc import WebCacheClient  # type: ignore
from typer import Typer

app = Typer()
wcc = WebCacheClient()


@app.command()
def fetch_file(filename: str) -> None:
    value = wcc.fetch_item(filename=filename)
    if value:
        print(os.path.join(os.getcwd(), value))
        wcc.remove_key(key=filename)


@app.command()
def fetch_value(key: str) -> None:
    value = wcc.fetch_item(key=key)
    print(value)
    if value:
        print(value)
        wcc.remove_key(key=key)


@app.command()
def cache_file(filename: str, force: bool = False) -> None:
    wcc.cache_item(filepath=filename, force=force)


@app.command()
def cache_value(key: str, value: str, force: bool = False) -> None:
    wcc.cache_item(key=key, value=value, force=force)


@app.command()
def keys(all: bool = False) -> None:
    result = wcc.get_keys(all=all)
    [print(x) for x in result]


@app.command()
def delete(key: str, exact: bool = False) -> None:
    wcc.remove_key(key, exact)
