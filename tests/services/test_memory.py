import time

import pytest

from my_cache_sdk.entities.user_context import UserContext
from my_cache_sdk.services.memory import InMemoryCache


@pytest.fixture
def memory_cache():
    return InMemoryCache(default_ttl=3600)


def test_memory_get(memory_cache):
    context = UserContext(customer_id="cust123", tenant_id="tenant456")
    memory_cache.set("test_key", "test_value", context)

    result = memory_cache.get("test_key", context)

    assert result == "test_value"


def test_memory_get_not_found(memory_cache):
    context = UserContext(customer_id="cust123", tenant_id="tenant456")

    result = memory_cache.get("non_existent_key", context)

    assert result is None


def test_memory_set_with_ttl(memory_cache):
    context = UserContext(customer_id="cust123", tenant_id="tenant456")

    memory_cache.set("test_key", "test_value", context, ttl=1)

    result = memory_cache.get("test_key", context)
    assert result == "test_value"

    time.sleep(2)
    result = memory_cache.get("test_key", context)
    assert result is None


def test_memory_delete(memory_cache):
    context = UserContext(customer_id="cust123", tenant_id="tenant456")
    memory_cache.set("test_key", "test_value", context)

    memory_cache.delete("test_key", context)

    result = memory_cache.get("test_key", context)
    assert result is None


def test_memory_default_ttl(memory_cache):
    context = UserContext(customer_id="cust123", tenant_id="tenant456")
    memory_cache.default_ttl = 1
    memory_cache.set("test_key", "test_value", context)
    result = memory_cache.get("test_key", context)
    assert result == "test_value"
    time.sleep(2)
    result = memory_cache.get("test_key", context)
    assert result is None
