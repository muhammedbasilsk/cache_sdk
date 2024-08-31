"""
Redis implementation of the CacheService.
"""

from typing import Any, Optional

import redis

from ..entities.user_context import UserContext
from ..interface_adapters.cache_service import CacheService


class RedisCache(CacheService):
    """
    Redis implementation of the CacheService.
    """

    def __init__(self, host: str, port: int, db: int = 0, default_ttl: int = 3600):
        """
        Initialize the Redis cache service.

        Args:
            host (str): The Redis server host.
            port (int): The Redis server port.
            db (int, optional): The Redis database number. Defaults to 0.
            default_ttl (int, optional): The default TTL in seconds. Defaults to 3600.
        """
        self.client = redis.Redis(host=host, port=port, db=db)
        self.default_ttl = default_ttl

    def _get_key(self, key: str, context: UserContext) -> str:
        """
        Generate a unique key based on the user context and provided key.

        Args:
            key (str): The key to retrieve.
            context (UserContext): The user context.

        Returns:
            str: A unique key string.
        """
        return f"{context.customer_id}:{context.tenant_id}:{key}"

    def get(self, key: str, context: UserContext) -> Optional[Any]:
        """
        Retrieve a value from the Redis cache.

        Args:
            key (str): The key to retrieve.
            context (UserContext): The user context.

        Returns:
            Optional[Any]: The value associated with the key, or None if not found.
        """
        full_key = self._get_key(key, context)
        value = self.client.get(full_key)
        return value.decode("utf-8") if value else None

    def set(
        self, key: str, value: Any, context: UserContext, ttl: Optional[int] = None
    ) -> None:
        """
        Set a value in the Redis cache.

        Args:
            key (str): The key to set.
            value (Any): The value to store.
            context (UserContext): The user context.
            ttl (Optional[int], optional): The TTL in seconds. Defaults to None.
        """
        full_key = self._get_key(key, context)
        self.client.setex(full_key, ttl or self.default_ttl, str(value))

    def delete(self, key: str, context: UserContext) -> None:
        """
        Delete a value from the Redis cache.

        Args:
            key (str): The key to delete.
            context (UserContext): The user context.
        """
        full_key = self._get_key(key, context)
        self.client.delete(full_key)
