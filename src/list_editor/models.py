from django.db import models
from django.contrib.postgres.fields import ArrayField

class AppModelVersion(models.Model):
    version = models.IntegerField()
    capture_datetime = models.DateTimeField("capture_date_time")

    @staticmethod
    def get_current_version(allow_none=False):
        try:
            last_version = AppModelVersion.objects.order_by("capture_datetime")[0]
        except IndexError as e:
            # no version saved yet.
            if not allow_none:
                raise e
            last_version = None
        return last_version

    def __str__(self):
        return str(self.version)


class Affiliations(models.Model):
    app_version = models.ForeignKey(AppModelVersion, on_delete=models.CASCADE)
    app_id = models.IntegerField()
    app_order = models.IntegerField()
    deck_size = models.IntegerField()
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=1000)
    icon = models.CharField(max_length=1000)
    is_team = models.BooleanField("Is Team?")
    eternal = models.BooleanField("Is Eternal?")
    only_allow_affiliation_characters = models.BooleanField()
    only_allow_affiliation_cards = models.BooleanField()
    only_allow_affiliation_keyword_characters = models.BooleanField()
    only_allow_affiliation_keyword_cards = models.BooleanField()
    affiliation_keyword_boss_must_be_leader = models.BooleanField()
    must_select_leader_as_boss = models.BooleanField()
    can_include_characters_with_same_name = models.BooleanField()
    affiliation_keyword_trait_ids = ArrayField(
        models.IntegerField()
    )

    def __str__(self):
        return f"{self.name} ({self.app_id})"

class Card(models.Model):
    app_version = models.ForeignKey(AppModelVersion, on_delete=models.CASCADE)
    app_id = models.IntegerField()
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=1000)
    objective_type_id = models.IntegerField(null=True)
    count = models.IntegerField()
    affiliation_id = models.IntegerField(null=True)
    preventing_trait_id = models.IntegerField(null=True)
    trait_id = models.IntegerField(null=True)
    rank_ids = ArrayField(
        models.IntegerField()
    )
    required_character_ids = ArrayField(
        models.IntegerField()
    )

    def __str__(self):
        return f"{self.name} ({self.app_id})"

