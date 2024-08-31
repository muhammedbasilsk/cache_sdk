"""
Abstract base class for cache services.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from ..entities.user_context import UserContext


class CacheService(ABC):
    """
    Abstract base class for cache services.
    """

    @abstractmethod
    def get(self, key: str, context: UserContext) -> Optional[Any]:
        """
        Retrieve a value from the cache.

        Args:
            key (str): The key to retrieve.
            context (UserContext): The user context.

        Returns:
            Optional[Any]: The value associated with the key, or None if not found.
        """
        pass

    @abstractmethod
    def set(
        self, key: str, value: Any, context: UserContext, ttl: Optional[int] = None
    ) -> None:
        """
        Set a value in the cache.

        Args:
            key (str): The key to set.
            value (Any): The value to store.
            context (UserContext): The user context.
            ttl (Optional[int]): Time to live in seconds. If None, use the default TTL.
        """
        pass

    @abstractmethod
    def delete(self, key: str, context: UserContext) -> None:
        """
        Delete a value from the cache.

        Args:
            key (str): The key to delete.
            context (UserContext): The user context.
        """
        pass
