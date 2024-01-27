from aiohttp import web
from bat_stats_api.routes import route_table
from bat_stats_api.data.entity.game_data_version_entity import GameDataVersionEntity


@route_table.get("/purge")
async def ping(request: web.Request) -> web.Response:

    print("Purging data.")
    await GameDataVersionEntity.all().delete()

    return web.Response(text="purge complete")


