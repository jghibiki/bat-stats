
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.postgres.fields import ArrayField

from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class Character(Model):
    id = fields.IntField(pk=True)
    game_data_version = fields.ForeignKeyField("models.GameDataVersion")
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


Character_Pydantic = pydantic_model_creator(Character)
Character_Pydantic_List = pydantic_queryset_creator(Character)


async def CharacterJson(c):
    return (
        await Character_Pydantic.from_tortoise_orm(c)
    ).model_dump_json()


async def CharacterJsonList(c):
    return (
        await Character_Pydantic_List.from_queryset(c)
    ).model_dump_json()
