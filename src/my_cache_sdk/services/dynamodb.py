"""
DynamoDB implementation of the CacheService.
"""

import time
from typing import Any, Optional

import boto3

from ..entities.user_context import UserContext
from ..interface_adapters.cache_service import CacheService


class DynamoDBCache(CacheService):
    """
    DynamoDB implementation of the CacheService.
    """

    def __init__(
        self, table_name: str, region_name: str = "us-east-1", default_ttl: int = 3600
    ):
        """
        Initialize the DynamoDB cache service.

        Args:
            table_name (str): The name of the DynamoDB table to use.
            region_name (str, optional): The AWS region name. Defaults to 'us-east-1'.
            default_ttl (int, optional): The default TTL in seconds. Defaults to 3600.
        """
        self.table = boto3.resource("dynamodb", region_name=region_name).Table(
            table_name
        )
        self.default_ttl = default_ttl

    def get(self, key: str, context: UserContext) -> Optional[Any]:
        """
        Retrieve a value from the DynamoDB cache.

        Args:
            key (str): The key to retrieve.
            context (UserContext): The user context.

        Returns:
            Optional[Any]: The value associated with the key, or None if not found.
        """
        response = self.table.get_item(
            Key={"PK": f"{context.customer_id}#{context.tenant_id}", "SK": key}
        )
        item = response.get("Item")
        if item and "expiry" in item:
            if item["expiry"] > int(time.time()):
                return item["value"]
            else:
                self.delete(key, context)
                return None
        return item["value"] if item else None

    def set(
        self, key: str, value: Any, context: UserContext, ttl: Optional[int] = None
    ) -> None:
        """
        Set a value in the DynamoDB cache.

        Args:
            key (str): The key to set.
            value (Any): The value to store.
            context (UserContext): The user context.
            ttl (Optional[int], optional): The TTL in seconds. Defaults to None.
        """
        expiry = int(time.time()) + (ttl or self.default_ttl)
        self.table.put_item(
            Item={
                "PK": f"{context.customer_id}#{context.tenant_id}",
                "SK": key,
                "value": value,
                "expiry": expiry,
            }
        )

    def delete(self, key: str, context: UserContext) -> None:
        """
        Delete a value from the DynamoDB cache.

        Args:
            key (str): The key to delete.
            context (UserContext): The user context.
        """
        self.table.delete_item(
            Key={"PK": f"{context.customer_id}#{context.tenant_id}", "SK": key}
        )
