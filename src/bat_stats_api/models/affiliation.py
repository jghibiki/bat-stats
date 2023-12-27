from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.postgres.fields import ArrayField
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator



class Affiliation(Model):
    id = fields.IntField(pk=True)
    game_data_version = fields.ForeignKeyField("models.GameDataVersion")
    app_id = fields.IntField()
    app_order = fields.IntField()
    deck_size = fields.IntField()
    name = fields.CharField(max_length=255)
    image = fields.CharField(max_length=1000)
    icon = fields.CharField(max_length=1000)
    is_team = fields.BooleanField()
    eternal = fields.BooleanField()
    only_allow_affiliation_characters = fields.BooleanField()
    only_allow_affiliation_cards = fields.BooleanField()
    only_allow_affiliation_keyword_characters = fields.BooleanField()
    only_allow_affiliation_keyword_cards = fields.BooleanField()
    affiliation_keyword_boss_must_be_leader = fields.BooleanField()
    must_select_leader_as_boss = fields.BooleanField()
    can_include_characters_with_same_name = fields.BooleanField()
    affiliation_keyword_trait_ids = ArrayField(
        element_type="int"
    )


Affiliation_Pydantic = pydantic_model_creator(Affiliation)
Affiliation_Pydantic_List = pydantic_queryset_creator(Affiliation)


async def Affiliation_Json(c):
    return (
        await Affiliation_Pydantic.from_tortoise_orm(c)
   ).model_dump_json()


async def Affiliation_Json_List(c):
    return (
        await Affiliation_Pydantic_List.from_queryset(c)
    ).model_dump_json()
