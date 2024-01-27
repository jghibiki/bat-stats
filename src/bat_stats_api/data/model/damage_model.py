from pydantic import BaseModel


class DamageModel(BaseModel):
    damage_type_name: str
    damage_type_id: int
    count: int
