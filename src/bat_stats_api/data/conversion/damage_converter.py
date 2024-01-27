from bat_stats_api.data.model.damage_model import DamageModel


async def to_model(damage_dict: dict) -> DamageModel:
    damage_type_id = damage_dict["damage_type_id"]
    damage_name = "blood" if damage_type_id == 1 else "stun"
    return DamageModel(
        damage_type_name=damage_name,
        damage_type_id=damage_type_id,
        count=damage_dict["count"]
    )