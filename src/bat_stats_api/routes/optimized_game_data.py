import datetime
import json

from aiohttp import web
from aiohttp.web_response import Response

from bat_stats_api.cache_manager import CacheManager
from bat_stats_api.data.conversion import character_converter
from bat_stats_api.data.entity.character_entity import CharacterEntity
from bat_stats_api.data.model.character_model import CharacterModel
from bat_stats_api.routes import route_table
from bat_stats_api.routes.util import get_app_version, apply_app_version_filter
from bat_stats_api.util.custom_dumps import custom_dumps
from bat_stats_api.util.paginate import paginate, PaginationResult

cache_manager = CacheManager.load()


@route_table.get("/optimized/character")
async def get_optimized_character(request: web.Request) -> web.Response:

    page = int(request.rel_url.query.get("page", 1))

    app_version = get_app_version(request)

    paginated: PaginationResult = await paginate(
        query=apply_app_version_filter(
            request=request,
            query=CharacterEntity.all().order_by("id")
        ),
        page_size=50,
        page=page
    )

    character_models = []

    async for character_entity in paginated.data.prefetch_related("game_data_version"):
        resource_name = f"character_{character_entity.app_id}_model"
        model_data = await cache_manager.get(
            app_version=app_version,
            resource_name=resource_name
        )

        if model_data is None:
            model: CharacterModel = await character_converter.to_model(character_entity)
            model_data = model.model_dump()
            await cache_manager.set(
                app_version=app_version,
                resource_name=resource_name,
                value=model_data
            )

        character_models.append(model_data)

    data = {
        "page": page,
        "total_pages": paginated.total_pages,
        "total_count": paginated.total_count,
        "data": character_models,
    }

    return web.json_response(
        data,
        dumps=lambda e: json.dumps(e, default=custom_dumps)
    )



@route_table.get("/optimized/cache/clear")
async def clear_cache(request: web.Request) -> web.Response:
    await cache_manager.clear()

    return web.Response(text="cache cleared")
