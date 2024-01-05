from typing import Protocol
from core_service import settings


class NoSQLStorageInterface(Protocol):
    provider_client = None

    def set(self, *args, **kwargs):
        ...

    def get(self, *args, **kwargs):
        ...


class RedisStorage(NoSQLStorageInterface):
    provider_client = RedisClient(...)

    def set(self, key: UUID, data: dict):
        self.provider_client.set(key, data)

    def get(self, key: UUID):
        self.provider_client.get(key)


class DynamoDBStorage(NoSQLStorageInterface):
    provider_client = DynamoDBClient(...)

    def set(self, key: UUID, data: dict):
        self.provider_client.set(key, data)

    def get(self, key: UUID):
        self.provider_client.get(key)


@singleton
def get_nosql_storage():
    provider = {
        "REDIS": RedisStorage,
        "DYNAMODB": DynamoDBStorage,
        "MONGODB": None
    }.get(settings.COMM_NOSQL_STORAGE_PROVIDER)
    return provider()