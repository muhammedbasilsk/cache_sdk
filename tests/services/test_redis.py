from unittest.mock import Mock, patch

import pytest

from my_cache_sdk.entities.user_context import UserContext
from my_cache_sdk.services.redis import RedisCache


@pytest.fixture
def mock_redis_client():
    return Mock()


@pytest.fixture
def redis_cache(mock_redis_client):
    with patch("redis.Redis", return_value=mock_redis_client):
        return RedisCache(host="localhost", port=6379, db=0)


def test_redis_get(redis_cache, mock_redis_client):
    context = UserContext(customer_id="cust123", tenant_id="tenant456")
    mock_redis_client.get.return_value = b"test_value"

    result = redis_cache.get("test_key", context)

    mock_redis_client.get.assert_called_once_with("cust123:tenant456:test_key")
    assert result == "test_value"


def test_redis_get_not_found(redis_cache, mock_redis_client):
    context = UserContext(customer_id="cust123", tenant_id="tenant456")
    mock_redis_client.get.return_value = None

    result = redis_cache.get("test_key", context)

    assert result is None


def test_redis_set_with_ttl(redis_cache, mock_redis_client):
    context = UserContext(customer_id="cust123", tenant_id="tenant456")
    redis_cache.set("test_key", "test_value", context, ttl=60)
    mock_redis_client.setex.assert_called_once_with(
        "cust123:tenant456:test_key", 60, "test_value"
    )


def test_redis_delete(redis_cache, mock_redis_client):
    context = UserContext(customer_id="cust123", tenant_id="tenant456")

    redis_cache.delete("test_key", context)

    mock_redis_client.delete.assert_called_once_with("cust123:tenant456:test_key")


def test_redis_default_ttl(redis_cache, mock_redis_client):
    context = UserContext(customer_id="cust123", tenant_id="tenant456")
    redis_cache.default_ttl = 3600
    redis_cache.set("test_key", "test_value", context)
    mock_redis_client.setex.assert_called_once_with(
        "cust123:tenant456:test_key", 3600, "test_value"
    )
