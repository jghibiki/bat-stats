
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.postgres.fields import ArrayField


class CharacterEntity(Model):
    id = fields.IntField(pk=True)
    app_id = fields.IntField()
    game_data_version = fields.ForeignKeyField("entity.GameDataVersionEntity", related_name="character")
    name = fields.CharField(max_length=255)
    alias = fields.CharField(max_length=255)
    affiliations = fields.JSONField()
    rival_affiliation_ids = ArrayField(
        element_type="int"
    )
    rank_ids = ArrayField(
        element_type="int"
    )
    weapon_ids = ArrayField(
        element_type="int"
    )
    image = fields.CharField(max_length=1000)
    background = fields.CharField(max_length=1000)
    willpower = fields.IntField()
    strength = fields.IntField()
    movement = fields.IntField()
    attack = fields.IntField()
    defense = fields.IntField()
    special = fields.IntField()
    endurance = fields.IntField()
    reputation = fields.IntField()
    funding = fields.IntField()
    eternal = fields.BooleanField()
    bases_size = fields.CharField(max_length=30)
    traits = fields.JSONField()
    linked_to_characters = ArrayField(
        element_type="int"
    )
    linked_characters = ArrayField(
        element_type="int"
    )
    shares_profile_in_game = fields.BooleanField()
    shares_equipment = fields.BooleanField()
    ignores_costs = fields.BooleanField()
    can_be_taken_individually = fields.BooleanField()
    adds_to_model_count = fields.BooleanField()
    adds_to_rank_count = fields.BooleanField(null=True)
    upgrade_ids = ArrayField(
        element_type="int"
    )

