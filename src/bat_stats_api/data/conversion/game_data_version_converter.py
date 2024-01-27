from bat_stats_api.data.entity.game_data_version_entity import GameDataVersionEntity
from bat_stats_api.data.model.game_data_version_model import GameDataVersionModel


async def to_model(entity: GameDataVersionEntity) -> GameDataVersionModel:
    return GameDataVersionModel(
        id=entity.id,
        capture_date_time=entity.capture_date_time
    )