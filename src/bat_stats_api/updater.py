import datetime
from typing import Optional
import aiohttp
import asyncio
from tortoise.exceptions import OperationalError
from tortoise.transactions import in_transaction
from tqdm import tqdm

from .models.game_data_version import GameDataVersion
from .models.affiliation import Affiliation
from .models.card import Card
from .models.character import Character


class PeriodicUpdater:
    def __init__(self):
        self.task: Optional[asyncio.Task] = None

    async def start_periodic_update(self, _):
        self.task = asyncio.create_task(self.periodic_update())

    async def periodic_update(self ):
        print("Starting periodic updater")
        while True:
            # trigger update
            print("Updater running.")
            await self.update()
            await asyncio.sleep(30)

    async def stop_periodic_update(self, _):
        print("Cancelling updater task.")
        self.task.cancel()
        await self.task
        print("Updater task returned.")

    async def update(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://app.knightmodels.com/version') as response:
                if response.status != 200:
                    print(f"Failed to update app data.\nStatus Code: {response.status}\nResponse:{response.text()}")

                data = await response.json()

            current_version = data["version"]
            print(f"API Reported version: {current_version}")
            previous_version: GameDataVersion = await GameDataVersion.all().order_by("-capture_date_time").first()

            if previous_version and current_version == previous_version.id:
                print(f"No update required. Current version matches previous version: {current_version}.")
                return
            else:
                print(f"Previous version: {previous_version}. Updating data.")

            async with session.get('https://app.knightmodels.com/gamedata') as response:
                if response.status != 200:
                    print(f"Failed to update app data.\nStatus Code: {response.status}\nResponse:{response.text()}")

                data = await response.json()

            print("Game data api request completed.")

            try:
                async with in_transaction():

                    version = GameDataVersion(
                        id=current_version,
                        capture_date_time = datetime.datetime.now()
                    )
                    await version.save()

                    print("Updating Affiliations")
                    for affiliation in tqdm(data["affiliations"]):
                        affiliation_data = {**affiliation}
                        del affiliation_data["id"]
                        affiliation_data["app_id"] = affiliation["id"]

                        a = Affiliation(
                            game_data_version_id=version.id,
                            **affiliation_data
                        )
                        await a.save()

                    print("Updating Cards")
                    for card in tqdm(data["cards"]):
                        card_data = {**card}
                        del card_data["id"]
                        card_data["app_id"] = card["id"]

                        c = Card(
                            game_data_version_id=version.id,
                            **card_data
                        )
                        await c.save()

                    print("Updating Character")
                    for character in tqdm(data["characters"]):
                        character_data = {**character}
                        del character_data["id"]
                        character_data["app_id"] = character["id"]

                        c = Character(
                            game_data_version_id=version.id,
                            **character_data
                        )
                        await c.save()

            except OperationalError as e:
                print(e)
                raise e

            print("Finished updating game data.")





