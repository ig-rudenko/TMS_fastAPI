import os

from .base import BaseCache
from .local import _local_cache
from .redis import _redis_cache


def get_cache() -> BaseCache:
    if os.getenv("REDIS_HOST"):
        return _redis_cache
    return _local_cache
