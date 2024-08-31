from typing import Any, Optional

from ...entities.user_context import UserContext
from ...frameworks.dynamodb.dynamodb_client import DynamoDBClient
from ..cache_service import CacheService


class DynamoDBRepository(CacheService):
    def __init__(self, client: DynamoDBClient):
        self.client = client

    def get(self, key: str, context: UserContext) -> Optional[Any]:
        return self.client.get_item(key, context)

    def set(self, key: str, value: Any, context: UserContext) -> None:
        self.client.put_item(key, value, context)

    def delete(self, key: str, context: UserContext) -> None:
        self.client.delete_item(key, context)
