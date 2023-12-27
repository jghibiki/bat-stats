from aiohttp import web
from bat_stats_api.routes import route_table
from bat_stats_api.models.game_data_version import GameDataVersion


@route_table.get("/purge")
async def ping(request: web.Request) -> web.Response:

    print("Purging data.")
    await GameDataVersion.all().delete()

    return web.Response(text="purge complete")


