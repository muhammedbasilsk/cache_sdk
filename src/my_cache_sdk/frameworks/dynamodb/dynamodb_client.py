from typing import Any, Optional

import boto3

from ...entities.user_context import UserContext
from ...exceptions import CacheException


class DynamoDBClient:
    def __init__(self, table_name: str, region_name: str):
        self.table = boto3.resource("dynamodb", region_name=region_name).Table(
            table_name
        )

    def get_item(self, key: str, context: UserContext) -> Optional[Any]:
        try:
            response = self.table.get_item(
                Key={"PK": f"{context.customer_id}#{context.tenant_id}", "SK": key}
            )
            item = response.get("Item")
            return item["value"] if item else None
        except Exception as e:
            raise CacheException(f"Failed to get item from DynamoDB: {str(e)}")

    def put_item(self, key: str, value: Any, context: UserContext) -> None:
        try:
            self.table.put_item(
                Item={
                    "PK": f"{context.customer_id}#{context.tenant_id}",
                    "SK": key,
                    "value": value,
                }
            )
        except Exception as e:
            raise CacheException(f"Failed to put item in DynamoDB: {str(e)}")

    def delete_item(self, key: str, context: UserContext) -> None:
        try:
            self.table.delete_item(
                Key={"PK": f"{context.customer_id}#{context.tenant_id}", "SK": key}
            )
        except Exception as e:
            raise CacheException(f"Failed to delete item from DynamoDB: {str(e)}")
