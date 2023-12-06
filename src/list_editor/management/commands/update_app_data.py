from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
import requests
import logging as log

from list_editor.models import AppModelVersion, Affiliation, Card, Equipment, Trait, Upgrade, Weapon, RuleDocument, Character

class Command(BaseCommand):
    help = "Updates the app data cache"

    def handle(self, *args, **options):
        response = requests.get("https://app.knightmodels.com/version")

        if response.status_code != 200:
            raise CommandError(f"Failed to load version.\nStatus Code: {response.status_code}\nError: {response.text}")

        current_version = response.json()["version"]
        self.stdout.write(f"API reports version: {current_version}")

        last_version = AppModelVersion.get_current_version(allow_none=True)
        self.stdout.write(f"Last version: {last_version}")

        if last_version is not None and current_version == last_version.version:
            # no update needed
            self.stdout.write(
                self.style.SUCCESS("No update required. Exiting cleanly."))
            return

        self.stdout.write("Updating app data cache.")

        with transaction.atomic():
            updated_version = AppModelVersion(
                version=current_version,
                capture_datetime=timezone.now()
            )
            updated_version.save()

            # if we're here we need to trigger an update.
            self.trigger_update(updated_version)


        self.stdout.write(
                self.style.SUCCESS('Successfully loaded app data.')
            )

    def trigger_update(self, version):
        response = requests.get("https://app.knightmodels.com/gamedata")

        if response != 200:
            pass  # throw exception

        data = response.json()

        for affiliation in data["affiliations"]:
            affiliation_data = {**affiliation}
            del affiliation_data["id"]
            affiliation_data["app_id"] = affiliation["id"]

            a = Affiliation(
                app_version=version,
                **affiliation_data
            )
            a.save()

        for card in data["cards"]:
            card_data = {**card}
            del card_data["id"]
            card_data["app_id"] = card["id"]

            card = Card(
                app_version=version,
                **card_data
            )
            card.save()

        for equipment in data["equipment"]:
            equipment_data = {**equipment}
            del equipment_data["id"]
            equipment_data["app_id"] = equipment["id"]

            equipment = Equipment(
                app_version=version,
                **equipment_data
            )
            equipment.save()

        for traits in data["traits"]:
            traits_data = {**traits}
            del traits_data["id"]
            traits_data["app_id"] = traits["id"]

            trait = Trait(
                app_version=version,
                **traits_data
            )
            trait.save()

        for upgrade in data["upgrades"]:
            upgrade_data = {**upgrade}
            del upgrade_data["id"]
            upgrade_data["app_id"] = upgrade["id"]

            upgrade = Upgrade(
                app_version=version,
                **upgrade_data
            )
            upgrade.save()

        for weapon in data["weapons"]:
            weapon_data = {**weapon}
            del weapon_data["id"]
            weapon_data["app_id"] = weapon["id"]

            weapon = Weapon(
                app_version=version,
                **weapon_data
            )
            weapon.save()

        for rule_document in data["rule_documents"]:
            rule_document_data = {**rule_document}
            del rule_document_data["id"]
            rule_document_data["app_id"] = rule_document["id"]

            rule_document = RuleDocument(
                app_version=version,
                **rule_document_data
            )
            rule_document.save()

        for character in data["characters"]:
            character_data = {**character}
            del character_data["id"]
            character_data["app_id"] = character["id"]

            character = Character(
                app_version=version,
                **character_data
            )
            character.save()
