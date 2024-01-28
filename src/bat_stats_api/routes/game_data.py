from aiohttp import web
from aiohttp.web_response import Response
from multidict import MultiDict
from bat_stats_api.routes import route_table


from bat_stats_api.data.entity.entity_serializer import EntitySerializer

from bat_stats_api.data.entity.affiliation_entity import AffiliationEntity
from bat_stats_api.data.entity.character_entity import CharacterEntity
from bat_stats_api.data.entity.game_data_version_entity import GameDataVersionEntity
from bat_stats_api.data.entity.weapon_entity import WeaponEntity
from bat_stats_api.routes.util import apply_app_version_filter


@route_table.get("/version")
async def get_latest_version(request: web.Request) -> Response:
    return web.Response(
        text=await EntitySerializer
            .get_instance()
            .game_data_version_to_json(
            await GameDataVersionEntity
                .all()
                .order_by("-capture_date_time")
                .first()
        ),
        headers=MultiDict({"CONTENT-TYPE": "application/json"})
    )

@route_table.get("/version/{id}")
async def get_latest_version(request: web.Request) -> Response:
    version_id = request.match_info["id"]
    return web.Response(
        text=await EntitySerializer
            .get_instance()
            .game_data_version_to_json(
            await GameDataVersionEntity
                .filter(id=version_id)
                .first()
        ),
        headers=MultiDict({"CONTENT-TYPE": "application/json"})
    )

@route_table.get("/affiliation")
async def get_affiliation(request: web.Request) -> web.Response:
    affiliations = (
        await EntitySerializer
            .get_instance()
            .affiliation_list_to_json(
            apply_app_version_filter(
                request,
                AffiliationEntity.all()
            )
        )
    ).model_dump_json()

    return web.Response(
        text=affiliations,
        headers=MultiDict({"CONTENT-TYPE": "application/json"})
    )


@route_table.get("/card")
async def get_card(request: web.Request) -> web.Response:
    cards = (
        await EntitySerializer
            .get_instance()
            .card_list_to_json(
            apply_app_version_filter(
                request,
                Card.all() # todo create card entity
            )
        )
    )

    return web.Response(
        text=cards,
        headers=MultiDict({"CONTENT-TYPE": "application/json"})
    )


@route_table.get("/character")
async def get_character(request: web.Request) -> web.Response:
    character = (
        await EntitySerializer
            .get_instance()
            .character_list_to_json(
            apply_app_version_filter(
                request,
                CharacterEntity.all()
            )
        )
    )

    return web.Response(
        text=character,
        headers=MultiDict({"CONTENT-TYPE": "application/json"})
    )


@route_table.get("/weapon")
async def get_character(request: web.Request) -> web.Response:
    weapons = (
        await EntitySerializer
            .get_instance()
            .weapon_list_to_json(
            apply_app_version_filter(
                request,
                WeaponEntity.all()
            )
        )
    )

    return web.Response(
        text=weapons,
        headers=MultiDict({"CONTENT-TYPE": "application/json"})
    )


@route_table.get("/trait")
async def get_trait(request: web.Request) -> web.Response:
    traits = (
        await EntitySerializer
            .get_instance()
            .trait_list_to_json(
            apply_app_version_filter(
                request,
                Trait.all() # TODO create trait entity
            )
        )
    )

    return web.Response(
        text=traits,
        headers=MultiDict({"CONTENT-TYPE": "application/json"})
    )
