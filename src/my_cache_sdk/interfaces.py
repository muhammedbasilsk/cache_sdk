from abc import ABC, abstractmethod
from typing import Any, Optional

from .context import UserContext


class CacheService(ABC):
    """
    Abstract base class for cache services.
    """

    @abstractmethod
    def get(self, key: str, context: UserContext) -> Optional[Any]:
        """
        Retrieve a value from the cache.

        Parameters
        ----------
        key : str
            The key to retrieve.
        context : UserContext
            The user context.

        Returns
        -------
        Optional[Any]
            The value associated with the key, or None if not found.
        """
        pass

    @abstractmethod
    def set(self, key: str, value: Any, context: UserContext) -> None:
        """
        Set a value in the cache.

        Parameters
        ----------
        key : str
            The key to set.
        value : Any
            The value to store.
        context : UserContext
            The user context.
        """
        pass

    @abstractmethod
    def delete(self, key: str, context: UserContext) -> None:
        """
        Delete a value from the cache.

        Parameters
        ----------
        key : str
            The key to delete.
        context : UserContext
            The user context.
        """
        pass
