import time

import boto3
import pytest
from moto import mock_dynamodb

from my_cache_sdk.cache import Cache
from my_cache_sdk.entities.user_context import UserContext


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    import os

    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="function")
def dynamodb(aws_credentials):
    with mock_dynamodb():
        yield boto3.resource("dynamodb", region_name="us-east-1")


@pytest.fixture(scope="function")
def dynamodb_table(dynamodb):
    table = dynamodb.create_table(
        TableName="test_table",
        KeySchema=[
            {"AttributeName": "PK", "KeyType": "HASH"},
            {"AttributeName": "SK", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "PK", "AttributeType": "S"},
            {"AttributeName": "SK", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    return table


def test_cache_initialization_dynamodb(dynamodb_table):
    cache = Cache(service="dynamodb", table_name="test_table", region_name="us-east-1")
    assert cache.service.__class__.__name__ == "DynamoDBCache"


def test_cache_initialization_redis():
    cache = Cache(service="redis", host="localhost", port=6379)
    assert cache.service.__class__.__name__ == "RedisCache"


def test_cache_initialization_memory():
    cache = Cache(service="memory")
    assert cache.service.__class__.__name__ == "InMemoryCache"


def test_cache_initialization_invalid():
    with pytest.raises(ValueError):
        Cache(service="invalid_service")


def test_cache_get(dynamodb_table):
    cache = Cache(service="dynamodb", table_name="test_table", region_name="us-east-1")
    context = UserContext(customer_id="cust123", tenant_id="tenant456")
    cache.set("test_key", "test_value", context)

    result = cache.get("test_key", context)

    assert result == "test_value"


def test_cache_set_with_ttl(dynamodb_table):
    cache = Cache(service="dynamodb", table_name="test_table", region_name="us-east-1")
    context = UserContext(customer_id="cust123", tenant_id="tenant456")

    cache.set("test_key", "test_value", context, ttl=1)

    result = cache.get("test_key", context)
    assert result == "test_value"

    time.sleep(2)
    result = cache.get("test_key", context)
    assert result is None


def test_cache_delete(dynamodb_table):
    cache = Cache(service="dynamodb", table_name="test_table", region_name="us-east-1")
    context = UserContext(customer_id="cust123", tenant_id="tenant456")
    cache.set("test_key", "test_value", context)

    cache.delete("test_key", context)

    result = cache.get("test_key", context)
    assert result is None


def test_cache_default_ttl(dynamodb_table):
    cache = Cache(
        service="dynamodb",
        table_name="test_table",
        region_name="us-east-1",
        default_ttl=1,
    )
    context = UserContext(customer_id="cust123", tenant_id="tenant456")

    cache.set("test_key", "test_value", context)

    result = cache.get("test_key", context)
    assert result == "test_value"

    time.sleep(2)
    result = cache.get("test_key", context)
    assert result is None
