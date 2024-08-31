from abc import ABC, abstractmethod
from typing import Any, Optional

from ..entities.user_context import UserContext


class CacheOperations(ABC):
    @abstractmethod
    def get(self, key: str, context: UserContext) -> Optional[Any]:
        pass

    @abstractmethod
    def set(self, key: str, value: Any, context: UserContext) -> None:
        pass

    @abstractmethod
    def delete(self, key: str, context: UserContext) -> None:
        pass
