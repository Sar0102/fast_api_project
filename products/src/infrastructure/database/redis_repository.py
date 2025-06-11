import aioredis

from core.transports import Product
from infrastructure.database.base import redis_client


class RedisRepository:
    def __init__(self, client: aioredis.Redis):
        self.client = client

    async def save(self, key: str, product: Product):
        await self.client.set(key, product.model_dump(mode='json'))

    async def list(self, key_pattern: str):
        cursor = 0
        keys = []
        while True:
            cursor, partial_keys = await self.client.scan(cursor, match=key_pattern)
            keys.extend(partial_keys)
            if cursor == 0:
                break
        return [Product.model_validate_json(await self.client.get(key)) for key in keys]


redis_repository = RedisRepository(redis_client)