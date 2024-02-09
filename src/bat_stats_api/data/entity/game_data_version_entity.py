from tortoise.models import Model
from tortoise import fields


class GameDataVersionEntity(Model):
    class PydanticMeta:
        backward_relations=False
        pass
    id = fields.IntField(pk=True)
    capture_date_time = fields.DatetimeField()

