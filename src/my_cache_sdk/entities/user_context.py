"""
User context module for cache operations.
"""

from dataclasses import dataclass


@dataclass
class UserContext:
    """
    Represents the user context for cache operations.

    Attributes:
        customer_id (str): The unique identifier for the customer.
        tenant_id (str): The unique identifier for the tenant.
    """

    customer_id: str
    tenant_id: str
