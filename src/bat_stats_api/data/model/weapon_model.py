from typing import List, Union

from pydantic import BaseModel

from bat_stats_api.data.model.damage_model import DamageModel
from bat_stats_api.data.model.game_data_version_model import GameDataVersionModel
from bat_stats_api.data.model.weapon_trait_model import WeaponTraitModel


class WeaponModel(BaseModel):
    id: int
    app_id: int
    game_data_version: GameDataVersionModel
    name: str
    rate_of_fire: Union[int, None]
    ammunition: Union[int, None]
    damage: List[DamageModel]
    traits: List[WeaponTraitModel]

