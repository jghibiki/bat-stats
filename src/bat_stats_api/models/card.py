
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.postgres.fields import ArrayField
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from bat_stats_api.models.enum_definitions import ObjectiveTypeId


class Card(Model):
    id = fields.IntField(pk=True)
    game_data_version = fields.ForeignKeyField("models.GameDataVersion")
    app_id = fields.IntField()
    name = fields.CharField(max_length=255)
    image = fields.CharField(max_length=1000)
    objective_type_id = fields.IntField(null=True)
    affiliation_id = fields.IntField(null=True)
    preventing_trait_id = fields.IntField(null=True)
    trait_id = fields.IntField(null=True)
    rank_ids = ArrayField(
        element_type="int"
    )
    required_character_ids = ArrayField(
        element_type="int"
    )


Card_Pydantic = pydantic_model_creator(Card)
Card_Pydantic_List = pydantic_queryset_creator(Card)


async def CardJson(c):
    return (
        await Card_Pydantic.from_tortoise_orm(c)
    ).model_dump_json()


async def CardJsonList(c):
    return (
        await Card_Pydantic_List.from_queryset(c)
    ).model_dump_json()
