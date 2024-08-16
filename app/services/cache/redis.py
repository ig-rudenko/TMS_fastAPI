import os
import pickle
from typing import Any

from redis import ConnectionPool, Redis

from .base import BaseCache


class RedisCache(BaseCache):

    def __init__(self, host: str, port: int, db: int, password: str | None = None, max_connections: int = 10):
        self._connections_pool = ConnectionPool(
            host=host,
            port=port,
            db=db,
            password=password,
            max_connections=max_connections,
        )
        self._redis = Redis(connection_pool=self._connections_pool)

    def get(self, key: str) -> Any:
        value: bytes = self._redis.get(key)
        print("GET LOCAL CACHE", key, value)
        if value is not None:
            return pickle.loads(value)
        return None

    def set(self, key: str, value: Any, expire: int):
        print("SET REDIS CACHE", key, value)
        self._redis.set(key, pickle.dumps(value), ex=expire)

    def delete(self, key: str):
        self._redis.delete(key)

    def clear(self):
        self._redis.flushdb()


REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

_redis_cache = RedisCache(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, max_connections=10
)
