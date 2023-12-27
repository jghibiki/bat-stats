from tortoise.models import Model
from tortoise import fields


class GameDataVersion(Model):
    id = fields.IntField(pk=True)
    capture_date_time = fields.DatetimeField()

