from pydantic import BaseModel

from bat_stats_api.data.model.game_data_version_model import GameDataVersionModel


class TraitModel(BaseModel):
    id: int
    app_id: int
    game_data_version: GameDataVersionModel
    name: str
    description: str
    sideboard_amount: int

