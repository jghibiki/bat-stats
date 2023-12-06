from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
import requests
import logging as log

from list_editor.models import AppModelVersion, Affiliations, Card

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

        with transaction.atomic():

            for affiliation in data["affiliations"]:
                affiliation_data = {**affiliation}
                del affiliation_data["id"]
                affiliation_data["app_id"] = affiliation["id"]

                a = Affiliations(
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
