from pydantic import BaseModel
from typing import List, Union

from bat_stats_api.data.model.character_affiliation_model import CharacterAffiliationModel
from bat_stats_api.data.model.character_rival_affiliation_model import CharacterRivalAffiliationModel
from bat_stats_api.data.model.character_trait_model import CharacterTraitModel
from bat_stats_api.data.model.game_data_version_model import GameDataVersionModel
from bat_stats_api.data.model.weapon_model import WeaponModel


class CharacterModel(BaseModel):
    id: int
    app_id: int
    game_data_version: GameDataVersionModel
    name: str
    alias: str
    affiliations: List[CharacterAffiliationModel]
    rival_affiliations: List[CharacterRivalAffiliationModel]
    rank_ids: List[int]
    weapons: List[WeaponModel]
    image: str
    background: str
    willpower: int
    strength: int
    movement: int
    attack: int
    defense: int
    special: int
    endurance: int
    reputation: int
    funding: int
    eternal: bool
    bases_sizes: str
    traits: List[CharacterTraitModel]
    linked_to_characters: List[int]
    linked_characters: List[int]
    shares_profile_in_game: bool
    shares_equipment: bool
    ignores_costs: bool
    can_be_taken_individually: bool
    adds_to_model_count: bool
    adds_to_rank_count: Union[bool, None]

    # i think upgrades can be skipped as all upgrades should have been replaced with alternate cards.
    #upgrades: List[]
