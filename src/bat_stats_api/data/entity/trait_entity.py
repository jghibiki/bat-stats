from tortoise.models import Model
from tortoise import fields


class TraitEntity(Model):
    id = fields.IntField(pk=True)
    app_id = fields.IntField()
    game_data_version = fields.ForeignKeyField("entity.GameDataVersionEntity", related_name="traits")
    name = fields.CharField(max_length=255)
    description = fields.CharField(max_length=5500)
    sideboard_amount = fields.IntField()

