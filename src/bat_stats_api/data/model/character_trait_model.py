from typing import Union

from pydantic import BaseModel

from bat_stats_api.data.model.trait_model import TraitModel

class CharacterTraitModel(BaseModel):
    alternative_name: Union[str, None]
    trait: TraitModel
