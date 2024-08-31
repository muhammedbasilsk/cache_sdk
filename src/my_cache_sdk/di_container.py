from dependency_injector import containers, providers

from .config import config
from .frameworks.dynamodb.dynamodb_client import DynamoDBClient
from .frameworks.redis.redis_client import RedisClient
from .interface_adapters.repositories.dynamodb_repository import DynamoDBRepository
from .interface_adapters.repositories.memory_repository import MemoryRepository
from .interface_adapters.repositories.redis_repository import RedisRepository
from .use_cases.cache_operations import CacheOperationsUseCase


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Clients
    dynamodb_client = providers.Singleton(
        DynamoDBClient,
        table_name=config.DYNAMODB_TABLE,
        region_name=config.DYNAMODB_REGION,
    )

    redis_client = providers.Singleton(
        RedisClient,
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.REDIS_DB,
    )

    # Repositories
    dynamodb_repository = providers.Singleton(
        DynamoDBRepository,
        client=dynamodb_client,
    )

    redis_repository = providers.Singleton(
        RedisRepository,
        client=redis_client,
    )

    memory_repository = providers.Singleton(MemoryRepository)

    # Use cases
    cache_operations = providers.Singleton(
        CacheOperationsUseCase,
        cache_service=providers.Selector(
            config.CACHE_SERVICE,
            dynamodb=dynamodb_repository,
            redis=redis_repository,
            memory=memory_repository,
        ),
    )


container = Container()
container.config.from_dict(config.__dict__)
