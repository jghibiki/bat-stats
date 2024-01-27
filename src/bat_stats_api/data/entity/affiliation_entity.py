from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.postgres.fields import ArrayField


class AffiliationEntity(Model):
    id = fields.IntField(pk=True)
    game_data_version = fields.ForeignKeyField("entity.GameDataVersionEntity", related_name="affiliation")
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

