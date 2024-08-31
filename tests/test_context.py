from my_cache_sdk.context import UserContext


def test_user_context():
    context = UserContext(customer_id="cust123", tenant_id="tenant456")
    assert context.customer_id == "cust123"
    assert context.tenant_id == "tenant456"
