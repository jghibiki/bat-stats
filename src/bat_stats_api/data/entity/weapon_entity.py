from tortoise.models import Model
from tortoise import fields


class WeaponEntity(Model):
    id = fields.IntField(pk=True)
    app_id = fields.IntField()
    game_data_version = fields.ForeignKeyField("entity.GameDataVersionEntity", related_name="weapon")
    name = fields.CharField(max_length=255)
    rate_of_fire = fields.IntField(null=True)
    ammunition = fields.IntField(null=True)
    damage = fields.JSONField()
    traits = fields.JSONField()

