from pydantic import BaseModel
from datetime import datetime

from bat_stats_api.data.model.game_data_version_model import GameDataVersionModel


class GameDataVersionModel(BaseModel):
    id: int
    game_data_version: GameDataVersionModel
    app_id: int
    app_order: int
    deck_size: int
    name
