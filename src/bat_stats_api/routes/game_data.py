from aiohttp import web
from multidict import MultiDict

from bat_stats_api.routes import route_table
from bat_stats_api.models.affiliation import Affiliation, Affiliation_Pydantic_List
from bat_stats_api.models.card import Card, CardJsonList
from bat_stats_api.models.character import Character, CharacterJsonList


@route_table.get("/affiliation")
async def get_affiliation(request: web.Request) -> web.Response:
    affiliations = (
        await Affiliation_Pydantic_List.from_queryset(
            Affiliation.all()
        )
    ).model_dump_json()

    return web.Response(
        text=affiliations,
        headers=MultiDict({"CONTENT-TYPE": "application/json"})
    )


@route_table.get("/card")
async def get_card(request: web.Request) -> web.Response:
    cards = (
        await CardJsonList(
            Card.all()
        )
    )

    return web.Response(
        text=cards,
        headers=MultiDict({"CONTENT-TYPE": "application/json"})
    )


@route_table.get("/character")
async def get_character(request: web.Request) -> web.Response:
    character = (
        await CharacterJsonList(
            Character.all()
        )
    )

    return web.Response(
        text=character,
        headers=MultiDict({"CONTENT-TYPE": "application/json"})
    )
