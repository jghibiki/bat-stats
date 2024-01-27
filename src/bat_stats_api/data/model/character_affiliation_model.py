from typing import List, Union

from pydantic import BaseModel


class CharacterAffiliationModel(BaseModel):
    id: int
    name: str
    can_be_team_boss: Union[bool, None]
    always_team_boss: Union[bool, None]
    rank_ids: List[int]
