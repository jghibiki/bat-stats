import asyncio
from aiohttp import web
from tortoise.contrib.aiohttp import register_tortoise

from bat_stats_api.routes import route_table
from bat_stats_api.updater import PeriodicUpdater


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

        register_tortoise(
            self.app,
            db_url="asyncpg://user:pass@localhost:5432/bat_stats",
            modules={"models": [
                "bat_stats_api.models.affiliation",
                "bat_stats_api.models.game_data_version",
                "bat_stats_api.models.card",
                "bat_stats_api.models.character",
            ]},
            generate_schemas=True
        )

        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        updater = PeriodicUpdater()
        self.app.on_startup.append(updater.start_periodic_update)
        self.app.on_shutdown.append(updater.stop_periodic_update)

    def run(self):
        """Starts the run of the aiohttp app."""
        web.run_app(self.app)
        print("App shutdown complete")




