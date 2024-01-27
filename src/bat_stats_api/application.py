import asyncio
from aiohttp import web
from tortoise.contrib.aiohttp import register_tortoise
import aiohttp_cors

from bat_stats_api.routes import route_table
from bat_stats_api.updater import PeriodicUpdater
from bat_stats_api.data.entity.entity_serializer import EntitySerializer


def get_app():
    return Application.load()


class Application:

    @staticmethod
    def load() -> "Application":
        if not hasattr(Application, "_instance"):
            Application._instance = Application()
        return Application._instance

    def __init__(self) -> None:

        self.app = web.Application()
        self.app.add_routes(route_table)

        cors = aiohttp_cors.setup(self.app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })

        # Configure CORS on all routes.
        for route in list(self.app.router.routes()):
            cors.add(route)

        register_tortoise(
            self.app,
            db_url="asyncpg://user:pass@localhost:5432/bat_stats",
            modules={"entity": [
                "bat_stats_api.data.entity.affiliation_entity",
                "bat_stats_api.data.entity.game_data_version_entity",
                "bat_stats_api.data.entity.card_entity",
                "bat_stats_api.data.entity.character_entity",
                "bat_stats_api.data.entity.weapon_entity",
                "bat_stats_api.data.entity.trait_entity",
            ]},
            generate_schemas=True
        )

        EntitySerializer()  # initialize serializers

        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        updater = PeriodicUpdater()
        self.app.on_startup.append(updater.start_periodic_update)
        self.app.on_shutdown.append(updater.stop_periodic_update)

    def run(self):
        """Starts the run of the aiohttp app."""
        web.run_app(self.app)
        print("App shutdown complete")




