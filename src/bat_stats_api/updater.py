import datetime
from typing import Optional
import aiohttp
import asyncio
from tortoise.exceptions import OperationalError
from tortoise.transactions import in_transaction
from tqdm import tqdm

from bat_stats_api.data.entity.game_data_version_entity import GameDataVersionEntity
from bat_stats_api.data.entity.affiliation_entity import AffiliationEntity
from bat_stats_api.data.entity.card_entity import CardEntity
from bat_stats_api.data.entity.character_entity import CharacterEntity
from bat_stats_api.data.entity.trait_entity import TraitEntity
from bat_stats_api.data.entity.weapon_entity import WeaponEntity


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
            previous_version: GameDataVersionEntity = await GameDataVersionEntity.all().order_by("-capture_date_time").first()

            if previous_version and current_version == previous_version.id:
                print(f"No update required. Current version matches previous version: {current_version.id}.")
                return
            else:
                print(f"Previous version: {previous_version.id}. Updating data.")

            async with session.get('https://app.knightmodels.com/gamedata') as response:
                if response.status != 200:
                    print(f"Failed to update app data.\nStatus Code: {response.status}\nResponse:{response.text()}")

                data = await response.json()

            print("Game data api request completed.")

            try:
                async with in_transaction():

                    version = GameDataVersionEntity(
                        id=current_version,
                        capture_date_time = datetime.datetime.now()
                    )
                    await version.save()

                    print("Updating Affiliations")
                    for affiliation in tqdm(data["affiliations"]):
                        affiliation_data = {**affiliation}
                        del affiliation_data["id"]
                        affiliation_data["app_id"] = affiliation["id"]

                        a = AffiliationEntity(
                            game_data_version_id=version.id,
                            **affiliation_data
                        )
                        await a.save()

                    print("Updating Cards")
                    for card in tqdm(data["cards"]):
                        card_data = {**card}
                        del card_data["id"]
                        card_data["app_id"] = card["id"]

                        c = CardEntity(
                            game_data_version_id=version.id,
                            **card_data
                        )
                        await c.save()

                    print("Updating Character")
                    for character in tqdm(data["characters"]):
                        character_data = {**character}
                        del character_data["id"]
                        character_data["app_id"] = character["id"]

                        c = CharacterEntity(
                            game_data_version_id=version.id,
                            **character_data
                        )
                        await c.save()

                    print("Updating Weapon")
                    for weapon in tqdm(data["weapons"]):
                        weapon_data = {**weapon}
                        del weapon_data["id"]
                        weapon_data["app_id"] = weapon["id"]

                        w = WeaponEntity(
                            game_data_version_id=version.id,
                            **weapon_data
                        )
                        await w.save()

                    print("Updating Trait")
                    for trait in tqdm(data["traits"]):
                        trait_data = {**trait}
                        del trait_data["id"]
                        trait_data["app_id"] = trait["id"]

                        t = TraitEntity(
                            game_data_version_id=version.id,
                            **trait_data
                        )
                        await t.save()

            except OperationalError as e:
                print(e)
                raise e
            except Exception as e:
                print(e)
                raise e

            print("Finished updating game data.")





