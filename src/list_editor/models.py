from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User


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


class Affiliation(models.Model):
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


class Equipment(models.Model):
    app_version = models.ForeignKey(AppModelVersion, on_delete=models.CASCADE)
    app_id = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    max_count = models.IntegerField()
    funding = models.IntegerField()
    reputation = models.IntegerField()
    image = models.CharField(max_length=1000, null=True)
    banned_character_ids = ArrayField(
        models.IntegerField()
    )
    banned_crew_equipment_ids = ArrayField(
        models.IntegerField()
    )
    required_character_ids = ArrayField(
        models.IntegerField()
    )
    required_crew_character_ids = ArrayField(
        models.IntegerField()
    )
    required_rank_ids = ArrayField(
        models.IntegerField()
    )
    required_affiliation_ids = ArrayField(
        models.IntegerField()
    )
    weapon_ids = ArrayField(
        models.IntegerField()
    )
    traits = ArrayField(
        models.JSONField()
    )
    willpower = models.IntegerField()
    strength = models.IntegerField()
    movement = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    special = models.IntegerField()
    endurance = models.IntegerField()
    ammunition = models.IntegerField()
    granted_weapon_id = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.name} ({self.app_id})"


class Trait(models.Model):
    app_version = models.ForeignKey(AppModelVersion, on_delete=models.CASCADE)
    app_id = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    sideboard_amount = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.app_id})"


class Upgrade(models.Model):
    app_version = models.ForeignKey(AppModelVersion, on_delete=models.CASCADE)
    app_id = models.IntegerField()
    rank_id = models.IntegerField(null=True)
    name = models.CharField(max_length=255)
    bases_size = models.CharField(max_length=30)
    image = models.CharField(max_length=1000)
    willpower = models.IntegerField()
    strength = models.IntegerField()
    movement = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    special = models.IntegerField()
    endurance = models.IntegerField()
    reputation = models.IntegerField()
    funding = models.IntegerField()
    eternal = models.BooleanField()
    weapon_ids = ArrayField(
        models.IntegerField()
    )
    traits = ArrayField(
        models.JSONField()
    )

    def __str__(self):
        return f"{self.name} ({self.app_id})"


class Weapon(models.Model):
    app_version = models.ForeignKey(AppModelVersion, on_delete=models.CASCADE)
    app_id = models.IntegerField()
    name = models.CharField(max_length=255)
    rate_of_fire = models.IntegerField(null=True)
    ammunition = models.IntegerField(null=True)
    damage = ArrayField(
        models.JSONField()
    )
    traits = ArrayField(
        models.JSONField()
    )

    def __str__(self):
        return f"{self.name} ({self.app_id})"


class Character(models.Model):
    app_version = models.ForeignKey(AppModelVersion, on_delete=models.CASCADE)
    app_id = models.IntegerField()
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    affiliations = ArrayField(
        models.JSONField()
    )
    rival_affiliation_ids = ArrayField(
        models.IntegerField()
    )
    rank_ids = ArrayField(
        models.IntegerField()
    )
    weapon_ids = ArrayField(
        models.IntegerField()
    )
    image = models.CharField(max_length=1000)
    background = models.CharField(max_length=1000)
    willpower = models.IntegerField()
    strength = models.IntegerField()
    movement = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    special = models.IntegerField()
    endurance = models.IntegerField()
    reputation = models.IntegerField()
    funding = models.IntegerField()
    eternal = models.IntegerField()
    bases_size = models.CharField(max_length=30)
    traits = ArrayField(
        models.JSONField()
    )
    linked_to_characters = ArrayField(
        models.IntegerField()
    )
    linked_characters = ArrayField(
        models.IntegerField()
    )
    shares_profile_in_game = models.BooleanField()
    shares_equipment = models.BooleanField()
    ignores_costs = models.BooleanField()
    can_be_taken_individually = models.BooleanField()
    adds_to_model_count = models.BooleanField()
    adds_to_rank_count = models.BooleanField()
    upgrade_ids = ArrayField(
        models.IntegerField()
    )

    def __str__(self):
        return f"{self.alias} [{self.name}] ({self.app_id})"


class RuleDocument(models.Model):
    app_version = models.ForeignKey(AppModelVersion, on_delete=models.CASCADE)
    app_id = models.IntegerField()
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.name} ({self.app_id})"


class Deck(models.Model):
    card_ids = ArrayField(
        models.IntegerField()
    )
    sideboard_ids = ArrayField(
        models.IntegerField()
    )


class CrewList(models.Model):
    affiliation = models.ForeignKey(Affiliation, on_delete=models.CASCADE)
    app_version = models.ForeignKey(AppModelVersion, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    notes = models.CharField(max_length=1000)
    deck = models.OneToOneField(Deck, name="deck", on_delete=models.CASCADE)
    list = models.JSONField()

    def __str__(self):
        return f"Crew: {self.name}"
