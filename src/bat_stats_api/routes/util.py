from aiohttp import web
from tortoise.queryset import QuerySet
from aiohttp.web_response import Response

from bat_stats_api.data.entity.game_data_version_entity import GameDataVersionEntity


def get_app_version(request: web.Request):
    return request.rel_url.query.get("app_version", None)


async def apply_app_version_filter(request: web.Request, query: QuerySet, fallback_to_latest=True) -> QuerySet:
    query_app_version = get_app_version(request)
    if query_app_version:
        return query.filter(game_data_version__id=query_app_version)

    if not fallback_to_latest:
        return query

    latest_app_version = (
        await GameDataVersionEntity
        .all()
        .order_by("-capture_date_time")
        .first()
    )

    return query.filter(game_data_version=latest_app_version.id)
