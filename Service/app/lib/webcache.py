from typing import Any

from app.schemas.schemas import RootCache

from .cache import Cache


class WebCache(Cache):
    def add_cache_item(self, key: str, value: Any) -> None:
        rc = self.load_cache()
        if rc is None:
            rc = RootCache(cache={key: value})
            self.save_cache(rc)
        else:
            rc.cache[key] = value
            self.save_cache(rc)

    def get_cache_item(self, key: str) -> Any:
        rc = self.load_cache()
        if rc is None:
            print("No cache")
            return None

        item = rc.cache.get(key, None)
        return item

    def remove_item(self, key: str) -> str:
        rc = self.load_cache()
        if rc is None:
            return "NA"

        item = rc.cache.get(key, None)
        if item:
            del rc.cache[key]
            self.save_cache(rc)
            return "OK"
        else:
            return "NA"

    def get_cache_keys(self) -> list[str]:
        rc = self.load_cache()
        if rc is None:
            return []

        keys = rc.cache.keys()
        return list(keys)


webcache = WebCache("/app/webcache", RootCache)


def get_webcache() -> WebCache:
    return webcache
