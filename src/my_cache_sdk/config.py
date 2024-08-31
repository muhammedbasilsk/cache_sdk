import os
from dataclasses import dataclass


@dataclass
class Config:
    CACHE_SERVICE: str = os.getenv("CACHE_SERVICE", "memory")
    DYNAMODB_TABLE: str = os.getenv("DYNAMODB_TABLE", "cache_table")
    DYNAMODB_REGION: str = os.getenv("DYNAMODB_REGION", "us-east-1")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    DEFAULT_TTL: int = int(os.getenv("DEFAULT_TTL", "3600"))  # Default 1 hour


config = Config()
