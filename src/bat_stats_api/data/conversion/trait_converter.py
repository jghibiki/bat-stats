from bat_stats_api.data.conversion import game_data_version_converter
from bat_stats_api.data.entity.trait_entity import TraitEntity
from bat_stats_api.data.model.trait_model import TraitModel


async def to_model(entity: TraitEntity) -> TraitModel:
    return TraitModel(
        id=entity.id,
        app_id=entity.app_id,
        game_data_version=await game_data_version_converter.to_model(entity.game_data_version),
        name=entity.name,
        description=entity.description,
        sideboard_amount=entity.sideboard_amount
    )
