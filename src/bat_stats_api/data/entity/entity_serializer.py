from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from tortoise.queryset import QuerySet

from .game_data_version_entity import GameDataVersionEntity
from .trait_entity import TraitEntity
from .weapon_entity import WeaponEntity
from .card_entity import CardEntity
from .character_entity import CharacterEntity
from .affiliation_entity import AffiliationEntity


class EntitySerializer:
    instance = None

    @staticmethod
    def get_instance():
        if not EntitySerializer.instance:
            EntitySerializer.instance = EntitySerializer()
        return EntitySerializer.instance

    def __init__(self):
        self._setup_weapon_serializer()
        self._setup_card_serializer()
        self._setup_character_serializer()
        self._setup_affiliation_serializer()
        self._setup_game_data_version_serializer()
        self._setup_trait_serializer()

    # Weapon serializers
    def _setup_weapon_serializer(self):
        self.weapon_pydantic = pydantic_model_creator(WeaponEntity)
        self.weapon_pydantic_list = pydantic_queryset_creator(WeaponEntity)

    async def weapon_to_json(self, c: WeaponEntity):
        return (
            await self.weapon_pydantic.from_tortoise_orm(c)
        ).model_dump_json()

    async def weapon_list_to_json(self, c: QuerySet):
        return (
            await self.weapon_pydantic_list.from_queryset(c)
        ).model_dump_json()


    # Card serializers
    def _setup_card_serializer(self):
        self.card_pydantic = pydantic_model_creator(CardEntity)
        self.card_pydantic_list = pydantic_queryset_creator(CardEntity)

    async def card_to_json(self, c: CardEntity):
        return (
            await self.card_pydantic.from_tortoise_orm(c)
        ).model_dump_json()

    async def card_list_to_json(self, c: QuerySet):
        return (
            await self.card_pydantic_list.from_queryset(c)
        ).model_dump_json()


    # Character serializers
    def _setup_character_serializer(self):
        self.character_pydantic = pydantic_model_creator(CharacterEntity)
        self.character_pydantic_list = pydantic_queryset_creator(CharacterEntity)

    async def character_to_json(self, c: CharacterEntity):
        return (
            await self.character_pydantic.from_tortoise_orm(c)
        ).model_dump_json()

    async def character_list_to_json(self, c: QuerySet):
        return (
            await self.character_pydantic_list.from_queryset(c)
        ).model_dump_json()

    # Affiliation serializers
    def _setup_affiliation_serializer(self):
        self.affiliation_pydantic = pydantic_model_creator(AffiliationEntity)
        self.affiliation_pydantic_list = pydantic_queryset_creator(AffiliationEntity)

    async def affiliation_to_json(self, c: AffiliationEntity):
        return (
            await self.affiliation_pydantic.from_tortoise_orm(c)
        ).model_dump_json()

    async def affiliation_list_to_json(self, c: QuerySet):
        return (
            await self.affiliation_pydantic_list.from_queryset(c)
        ).model_dump_json()

    # GameDataVersion serializers
    def _setup_game_data_version_serializer(self):
        self.game_data_version_pydantic = pydantic_model_creator(GameDataVersionEntity)
        self.game_data_version_pydantic_list = pydantic_queryset_creator(GameDataVersionEntity)

    async def game_data_version_to_json(self, c: GameDataVersionEntity):
        return (
            await self.game_data_version_pydantic.from_tortoise_orm(c)
        ).model_dump_json()

    async def game_data_version_list_to_json(self, c: QuerySet):
        return (
            await self.game_data_version_pydantic_list.from_queryset(c)
        ).model_dump_json()

    # Trait serializers
    def _setup_trait_serializer(self):
        self.trait_pydantic = pydantic_model_creator(TraitEntity)
        self.trait_pydantic_list = pydantic_queryset_creator(TraitEntity)

    async def trait_to_json(self, c: TraitEntity):
        return (
            await self.trait_pydantic.from_tortoise_orm(c)
        ).model_dump_json()

    async def trait_list_to_json(self, c: QuerySet):
        return (
            await self.trait_pydantic_list.from_queryset(c)
        ).model_dump_json()
