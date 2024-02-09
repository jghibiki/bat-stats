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


def character_key(app_version, character_id):
    return f"character_{character_id}_model"


async def load_character(app_version, character_id):
    resource_name = character_key(app_version, character_id)
    model_data = await cache_manager.get(
        app_version=app_version,
        resource_name=resource_name
    )
    return model_data


async def cache_character(app_version, character_id, entity):
    resource_name = character_key(app_version, character_id)
    model: CharacterModel = await character_converter.to_model(entity)
    model_data = model.model_dump()
    await cache_manager.set(
        app_version=app_version,
        resource_name=resource_name,
        value=model_data
    )
    return model_data


@route_table.get("/optimized/character")
async def get_optimized_character(request: web.Request) -> web.Response:

    page = int(request.rel_url.query.get("page", 1))
    app_version = get_app_version(request)

    page_resouce = f"optimized_character_page_{page}"
    page_data = await cache_manager.get(
        app_version=app_version,
        resource_name=page_resouce
    )

    if page_data is not None:
        return web.Response(
            headers={
                "content-type": "application/json"
            },
            text=page_data
        )

    paginated: PaginationResult = await paginate(
        query=apply_app_version_filter(
            request=request,
            query=apply_app_version_filter(
                request,
                CharacterEntity.all().order_by("id")
            )
        ),
        page_size=50,
        page=page
    )

    character_models = []

    async for character_entity in paginated.data.prefetch_related("game_data_version"):
        model_data = await load_character(character_entity.app_id)

        if model_data is None:
            model_data = cache_character(app_version, character_entity.app_id, character_entity)

        character_models.append(model_data)

    data = {
        "page": page,
        "total_pages": paginated.total_pages,
        "total_count": paginated.total_count,
        "data": character_models,
    }

    data_text = json.dumps(
        data, default=custom_dumps
    )

    await cache_manager.set(
        app_version=app_version,
        resource_name=page_resouce,
        value=data_text
    )

    return web.Response(
        headers={
            "Content-Type": "application/json",
        },
        text=data_text
    )

@route_table.get("/optimized/character/id/{id}")
async def get_optimized_character_by_id(request: web.Request) -> web.Response:
    character_id = request.match_info["id"]
    app_version = get_app_version(request)
    model_data = await load_character(app_version, character_id)

    if model_data is None:
        character_entity = await apply_app_version_filter(
            request,
            CharacterEntity.filter(app_id=character_id)
        ).first().prefetch_related("game_data_version")
        model_data = await cache_character(app_version, character_entity.app_id, character_entity)

    data_text = json.dumps(
        model_data, default=custom_dumps
    )

    return web.Response(
        headers={
            "Content-Type": "application/json",
        },
        text=data_text
    )


@route_table.get("/optimized/character/precache")
async def precache_optimized_characters(request: web.Request) -> web.Response:
    app_version = get_app_version(request)

    character_entities = apply_app_version_filter(
        request,
        CharacterEntity.all()
    ).prefetch_related("game_data_version")

    async for character_entity in character_entities:
        await cache_character(app_version, character_entity.id, character_entity)


    return web.Response(
        text="models cached."
    )



@route_table.get("/optimized/cache/clear")
async def clear_cache(request: web.Request) -> web.Response:
    await cache_manager.clear()

    return web.Response(text="cache cleared")
