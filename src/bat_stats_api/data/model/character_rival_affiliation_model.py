from typing import List

from pydantic import BaseModel


class CharacterRivalAffiliationModel(BaseModel):
    id: int
    name: str
