"""
Main cache module providing a unified interface for different cache services.
"""

from typing import Any, Optional

from .config import config
from .entities.user_context import UserContext
from .services.dynamodb import DynamoDBCache
from .services.memory import InMemoryCache
from .services.redis import RedisCache


class Cache:
    """
    Main cache class that provides a unified interface for different cache services.
    """

    def __init__(self, service: str, default_ttl: Optional[int] = None, **kwargs):
        """
        Initialize the cache with the specified service.

        Args:
            service (str): The name of the cache service to use
                ('dynamodb', 'redis', or 'memory').
            default_ttl (Optional[int]): Default Time to Live in seconds.
                If None, use the value from config.
            **kwargs: Additional keyword arguments for the specific cache service.

        Raises:
            ValueError: If an invalid cache service is specified.
        """
        self.default_ttl = default_ttl or config.DEFAULT_TTL

        if service == "dynamodb":
            self.service = DynamoDBCache(default_ttl=self.default_ttl, **kwargs)
        elif service == "redis":
            self.service = RedisCache(default_ttl=self.default_ttl, **kwargs)
        elif service == "memory":
            self.service = InMemoryCache(default_ttl=self.default_ttl)
        else:
            raise ValueError("Invalid cache service specified")

    def get(self, key: str, context: UserContext) -> Optional[Any]:
        """
        Retrieve a value from the cache.

        Args:
            key (str): The key to retrieve.
            context (UserContext): The user context.

        Returns:
            Optional[Any]: The value associated with the key, or None if not found.
        """
        return self.service.get(key, context)

    def set(
        self, key: str, value: Any, context: UserContext, ttl: Optional[int] = None
    ) -> None:
        """
        Set a value in the cache.

        Args:
            key (str): The key to set.
            value (Any): The value to store.
            context (UserContext): The user context.
            ttl (Optional[int]): Time to Live in seconds. If None, use the default TTL.
        """
        self.service.set(key, value, context, ttl=ttl)

    def delete(self, key: str, context: UserContext) -> None:
        """
        Delete a value from the cache.

        Args:
            key (str): The key to delete.
            context (UserContext): The user context.
        """
        self.service.delete(key, context)
