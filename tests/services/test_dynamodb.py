import time

import boto3
import pytest
from moto import mock_dynamodb

from my_cache_sdk.entities.user_context import UserContext
from my_cache_sdk.services.dynamodb import DynamoDBCache


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


@pytest.fixture
def dynamodb_cache(dynamodb_table):
    return DynamoDBCache(table_name="test_table", region_name="us-east-1")


def test_dynamodb_get(dynamodb_cache):
    context = UserContext(customer_id="cust123", tenant_id="tenant456")
    dynamodb_cache.set("test_key", "test_value", context)

    result = dynamodb_cache.get("test_key", context)

    assert result == "test_value"


def test_dynamodb_get_not_found(dynamodb_cache):
    context = UserContext(customer_id="cust123", tenant_id="tenant456")

    result = dynamodb_cache.get("non_existent_key", context)

    assert result is None


def test_dynamodb_set_with_ttl(dynamodb_cache):
    context = UserContext(customer_id="cust123", tenant_id="tenant456")
    dynamodb_cache.set("test_key", "test_value", context, ttl=1)
    result = dynamodb_cache.get("test_key", context)
    assert result == "test_value"
    time.sleep(2)
    result = dynamodb_cache.get("test_key", context)
    assert result is None


def test_dynamodb_default_ttl(dynamodb_cache):
    context = UserContext(customer_id="cust123", tenant_id="tenant456")
    dynamodb_cache.default_ttl = 1
    dynamodb_cache.set("test_key", "test_value", context)
    result = dynamodb_cache.get("test_key", context)
    assert result == "test_value"
    time.sleep(2)
    result = dynamodb_cache.get("test_key", context)
    assert result is None


def test_dynamodb_delete(dynamodb_cache):
    context = UserContext(customer_id="cust123", tenant_id="tenant456")
    dynamodb_cache.set("test_key", "test_value", context)

    dynamodb_cache.delete("test_key", context)

    result = dynamodb_cache.get("test_key", context)
    assert result is None
