from aiohttp import web
from aiohttp.web_routedef import RouteTableDef

route_table: RouteTableDef = web.RouteTableDef()

__all__ = [
    "ping",
    "game_data",
    "debug",
    "optimized_game_data",
]
from bat_stats_api.routes import *


