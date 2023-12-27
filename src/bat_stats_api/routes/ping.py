from aiohttp import web
from bat_stats_api.routes import route_table


@route_table.get("/ping")
async def ping(request: web.Request) -> web.Response:
    return web.Response(text="pong")


