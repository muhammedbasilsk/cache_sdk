from typing import Any, Optional

from ..entities.user_context import UserContext
from ..interface_adapters.cache_service import CacheService
from .interfaces import CacheOperations


class CacheOperationsUseCase(CacheOperations):
    def __init__(self, cache_service: CacheService):
        self.cache_service = cache_service

    def get(self, key: str, context: UserContext) -> Optional[Any]:
        return self.cache_service.get(key, context)

    def set(self, key: str, value: Any, context: UserContext) -> None:
        self.cache_service.set(key, value, context)

    def delete(self, key: str, context: UserContext) -> None:
        self.cache_service.delete(key, context)
