from typing import List

from bat_stats_api.data.conversion import game_data_version_converter, damage_converter, trait_converter
from bat_stats_api.data.entity.affiliation_entity import AffiliationEntity
from bat_stats_api.data.entity.character_entity import CharacterEntity
from bat_stats_api.data.entity.trait_entity import TraitEntity
from bat_stats_api.data.entity.weapon_entity import WeaponEntity
from bat_stats_api.data.model.character_affiliation_model import CharacterAffiliationModel
from bat_stats_api.data.model.character_model import CharacterModel
from bat_stats_api.data.model.character_rival_affiliation_model import CharacterRivalAffiliationModel
from bat_stats_api.data.model.character_trait_model import CharacterTraitModel
from bat_stats_api.data.model.weapon_model import WeaponModel
from bat_stats_api.data.model.weapon_trait_model import WeaponTraitModel


async def to_model(entity: CharacterEntity) -> CharacterModel:
    character_affiliations = await _generate_character_affiliations(entity.affiliations)
    rival_affiliations = await _generate_character_rival_affiliations(entity.rival_affiliation_ids)
    weapons = await _generate_weapons(entity.weapon_ids)
    character_traits = await _generate_character_traits(entity.traits)

    return CharacterModel(
        id=entity.id,
        app_id=entity.app_id,
        game_data_version=await game_data_version_converter.to_model(entity.game_data_version),
        name=entity.name,
        alias=entity.alias,
        affiliations=character_affiliations,
        rival_affiliations=rival_affiliations,
        rank_ids=entity.rank_ids,
        weapons=weapons,
        image=entity.image,
        background=entity.background,
        willpower=entity.willpower,
        strength=entity.strength,
        movement=entity.movement,
        attack=entity.attack,
        defense=entity.defense,
        special=entity.special,
        endurance=entity.endurance,
        reputation=entity.reputation,
        funding=entity.funding,
        eternal=entity.eternal,
        bases_sizes=entity.bases_size,
        traits=character_traits,
        linked_to_characters=entity.linked_to_characters,
        linked_characters=entity.linked_characters,
        shares_profile_in_game=entity.shares_profile_in_game,
        shares_equipment=entity.shares_equipment,
        ignores_costs=entity.ignores_costs,
        can_be_taken_individually=entity.can_be_taken_individually,
        adds_to_model_count=entity.adds_to_model_count,
        adds_to_rank_count=entity.adds_to_rank_count
    )


async def _generate_character_affiliations(affiliations: List[dict]) -> List[CharacterAffiliationModel]:
    mapped = []

    affiliation_metadata = {e["affiliation_id"]: e for e in affiliations}
    query = AffiliationEntity.filter(app_id__in=affiliation_metadata.keys())
    async for raw_affiliation in query.prefetch_related():
        metadata = affiliation_metadata[raw_affiliation.app_id]

        new_model = CharacterAffiliationModel(
            id=raw_affiliation.id,
            name=raw_affiliation.name,
            can_be_team_boss=metadata["can_be_team_boss"],
            always_team_boss=metadata["always_team_boss"],
            rank_ids=metadata["rank_ids"]
        )

        mapped.append(new_model)
    return mapped


async def _generate_character_rival_affiliations(affiliations: List[int]) -> List[CharacterRivalAffiliationModel]:
    mapped = []

    query = AffiliationEntity.filter(app_id__in=affiliations)
    async for raw_affiliation in query.prefetch_related():
        new_model = CharacterRivalAffiliationModel(
            id=raw_affiliation.id,
            name=raw_affiliation.name
        )

        mapped.append(new_model)
    return mapped


async def _generate_weapons(weapon_ids: List[int]) -> List[CharacterAffiliationModel]:
    mapped = []

    query = WeaponEntity.filter(app_id__in=weapon_ids)
    async for raw_weapon in query.prefetch_related("game_data_version"):
        weapon_traits = await _generate_weapon_traits(raw_weapon.traits)

        damage = [
            await damage_converter.to_model(damage)
            for damage in raw_weapon.damage
        ]

        new_model = WeaponModel(
            id=raw_weapon.id,
            app_id=raw_weapon.app_id,
            game_data_version=await game_data_version_converter.to_model(raw_weapon.game_data_version),
            name=raw_weapon.name,
            rate_of_fire=raw_weapon.rate_of_fire,
            ammunition=raw_weapon.ammunition,
            damage=damage,
            traits=weapon_traits
        )

        mapped.append(new_model)
    return mapped


async def _generate_weapon_traits(trait_metadata: List[dict]) -> List[WeaponTraitModel]:
    mapped = []
    trait_map = { e["trait_id"]: e["alternate_name"] for e in trait_metadata}
    query = TraitEntity.filter(app_id__in=trait_map.keys())
    async for raw_trait in query.prefetch_related("game_data_version"):
        new_model = WeaponTraitModel(
            alternative_name=trait_map[raw_trait.app_id],
            trait=await trait_converter.to_model(raw_trait)
        )
        mapped.append(new_model)

    return mapped


async def _generate_character_traits(trait_metadata: List[dict]) -> List[CharacterTraitModel]:
    mapped = []
    trait_map = { e["trait_id"]: e["alternate_name"] for e in trait_metadata}
    query = TraitEntity.filter(app_id__in=trait_map.keys())
    async for raw_trait in query.prefetch_related("game_data_version"):
        new_model = CharacterTraitModel(
            alternative_name = trait_map[raw_trait.app_id],
            trait=await trait_converter.to_model(raw_trait)
        )
        mapped.append(new_model)

    return mapped
