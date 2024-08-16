from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from .base import BaseCache


@dataclass
class CacheValue:
    value: Any
    exp: datetime


class LocalCache(BaseCache):

    def __init__(self):
        self._cache: dict[str, CacheValue] = {}

    def get(self, key: str) -> Any:
        print("GET LOCAL CACHE", key)

        if key in self._cache and self._cache[key].exp > datetime.now():
            return self._cache[key].value
        else:
            self.delete(key)
        return None

    def set(self, key: str, value: Any, expire: int):
        print("SET LOCAL CACHE", key, value)
        self._cache[key] = CacheValue(value=value, exp=datetime.now() + timedelta(expire))

    def delete(self, key: str):
        try:
            del self._cache[key]
        except KeyError:
            pass

    def clear(self):
        self._cache = {}


_local_cache = LocalCache()
