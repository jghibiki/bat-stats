from tortoise import fields
from tortoise.models import Model

class AffiliationEntity(Model):
    id = fields.IntField(pk=True)
    value = fields.BinaryField()
