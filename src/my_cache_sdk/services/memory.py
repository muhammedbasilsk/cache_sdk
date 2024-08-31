"""
In-memory implementation of the CacheService.
"""

import time
from typing import Any, Dict, Optional

from ..entities.user_context import UserContext
from ..interface_adapters.cache_service import CacheService


class InMemoryCache(CacheService):
    """
    In-memory implementation of the CacheService.
    """

    def __init__(self, default_ttl: int):
        """
        Initialize the in-memory cache service.

        Args:
            default_ttl (int): Default Time to Live in seconds.
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
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
        return f"{context.customer_id}#{context.tenant_id}#{key}"

    def get(self, key: str, context: UserContext) -> Optional[Any]:
        """
        Retrieve a value from the in-memory cache.

        Args:
            key (str): The key to retrieve.
            context (UserContext): The user context.

        Returns:
            Optional[Any]: The value associated with the key, or None if not found
            or expired.
        """
        full_key = self._get_key(key, context)
        item = self.cache.get(full_key)
        if item and item["expiry"] > time.time():
            return item["value"]
        if item:
            del self.cache[full_key]
        return None

    def set(
        self, key: str, value: Any, context: UserContext, ttl: Optional[int] = None
    ) -> None:
        """
        Set a value in the in-memory cache.

        Args:
            key (str): The key to set.
            value (Any): The value to store.
            context (UserContext): The user context.
            ttl (Optional[int]): Time to Live in seconds. If None, use the default TTL.
        """
        full_key = self._get_key(key, context)
        expiry = time.time() + (ttl or self.default_ttl)
        self.cache[full_key] = {"value": value, "expiry": expiry}

    def delete(self, key: str, context: UserContext) -> None:
        """
        Delete a value from the in-memory cache.

        Args:
            key (str): The key to delete.
            context (UserContext): The user context.
        """
        full_key = self._get_key(key, context)
        self.cache.pop(full_key, None)
