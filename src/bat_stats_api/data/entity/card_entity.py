
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.postgres.fields import ArrayField


class CardEntity(Model):
    id = fields.IntField(pk=True)
    game_data_version = fields.ForeignKeyField("entity.GameDataVersionEntity", related_name="card")
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
