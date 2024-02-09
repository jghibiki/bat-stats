import asyncio
import json

from aiocache import Cache
from aiocache.serializers import JsonSerializer, PickleSerializer

from bat_stats_api.util.custom_dumps import custom_dumps


class CacheManager:
    __instance__ = None

    def __init__(self):
        self.cache = Cache()

    @staticmethod
    def load():
        if CacheManager.__instance__ is None:
            CacheManager.__instance__ = CacheManager()
        return CacheManager.__instance__

    def calculate_key(self, app_version: int, resource_name: str) -> str:
        return f"{app_version}_{resource_name}"

    async def cache_by_app_version_and_resource(self, app_version: int, resource_name: str, load_func ):
        cache_key = self.calculate_key(app_version, resource_name)

        cache_result = await self.cache.get(cache_key)
        if cache_result is None:
            entity = await load_func()
            await self.cache.set(cache_key, entity)
            return entity
        else:
            return cache_result

    async def get(self, app_version: int, resource_name: str):
        cache_key = self.calculate_key(app_version, resource_name)
        return await self.cache.get(cache_key)

    async def set(self, app_version: int, resource_name: str, value: str):
        cache_key = self.calculate_key(app_version, resource_name)

        return await self.cache.set(
            cache_key,
            value,
        )

    async def clear(self):
        await self.cache.clear()