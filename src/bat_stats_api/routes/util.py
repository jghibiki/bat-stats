from aiohttp import web
from tortoise.queryset import QuerySet
from aiohttp.web_response import Response

def get_app_version(request: web.Request):
    return request.rel_url.query.get("app_version", None)


def apply_app_version_filter(request: web.Request, query: QuerySet) -> QuerySet:
    app_version = get_app_version(request)
    if app_version:
        return query.filter(game_data_version__id=app_version)
    else:
        return query
