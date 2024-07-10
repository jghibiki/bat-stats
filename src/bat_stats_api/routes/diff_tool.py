from textwrap import dedent
from datetime import datetime

from aiohttp import web
from diff_match_patch import diff_match_patch

from bat_stats_api.data.entity.game_data_version_entity import GameDataVersionEntity
from bat_stats_api.routes import route_table

@route_table.get("/diff/version/list")
async def diff(request: web.Request) -> web.Response:
    versions = [ e.id for e in await GameDataVersionEntity.all()]

    return web.json_response(data=versions)

@route_table.get("/diff")
async def diff(request: web.Request) -> web.Response:
    base_version_id = request.rel_url.query.get("base", None)
    alt_version_id = request.rel_url.query.get("alt", None)

    base_version = await GameDataVersionEntity.filter(id=base_version_id).first().prefetch_related("affiliation", "weapon")
    alt_version = await GameDataVersionEntity.filter(id=alt_version_id).first().prefetch_related("affiliation", "weapon")

    if base_version is None:
       raise Exception(f"unable to find base version: {base_version}")

    if alt_version is None:
        raise Exception(f"unable to find alt version: {alt_version}")


    (traits_changed, trait_change_log) = await generate_trait_diff_log(base_version, alt_version)

    (characters_changed, character_change_log) = await generate_character_diff_log(base_version, alt_version)

    (weapons_changed, weapon_change_log) = await generate_weapon_diff_log(base_version, alt_version)

    diff_log = trait_change_log + character_change_log + weapon_change_log
    has_change = traits_changed or characters_changed or weapons_changed

    if has_change: diff_log = "<div>Detected changes!</div><br/>" + diff_log
    else:
        diff_log = "<div>No changes detected!</div><br/>"

    base_date = datetime.fromtimestamp(int(base_version_id)).strftime("%Y-%m-%d %H:%M:%S")
    alt_date = datetime.fromtimestamp(int(alt_version_id)).strftime("%Y-%m-%d %H:%M:%S")

    response = f"""
    <html>
        <body>
        <h3>
            Showing difference between version {base_version_id} ({base_date}) and {alt_version_id} ({alt_date})
        </h3>
        </br>
        {diff_log} 
        </body> 
    </html> 
    """

    return web.Response(text=response, content_type="text/html")



async def generate_trait_diff_log(base_version, alt_version) -> (bool, str):
    pairs = {}
    diff_log = ""
    has_change = False

    async for base_trait in base_version.traits.all():
        if base_trait.app_id in pairs:
            pair = pairs[base_trait.app_id]
        else:
            pair = {}
        pair["base"] = base_trait
        pairs[base_trait.app_id] = pair

    async for alt_trait in alt_version.traits.all():
        if alt_trait.app_id in pairs:
            pair = pairs[alt_trait.app_id]
        else:
            pair = {}
        pair["alt"] = alt_trait
        pairs[alt_trait.app_id] = pair


    for pair in pairs.values():
        base = pair.get("base")
        alt = pair.get("alt")

        if base is None and alt is not None:
            has_change = True
            diff_log += dedent(f"""
            <b>Trait Added: {alt.name}</b>
            <div>Description: {alt.description}</div>
            <br/>
            """).strip() + "\n\n"
        elif base is not None and alt is None:
            has_change = True
            diff_log += dedent(f"""
            <b>Trait Removed: {base.name}</b>
            <div>Description: {base.description}</div>
            </br>
            """).strip() + "\n\n"
        elif base is not None and alt is not None:

            if base.description.lower() == alt.description.lower():
                continue

            has_change = True
            dmp = diff_match_patch()

            diffs = dmp.diff_main(
                base.description,
                alt.description
            )
            dmp.diff_cleanupSemantic(diffs)
            diff = dmp.diff_prettyHtml(diffs)

            diff_log += f"""
            <b>Trait Updated: {base.name} </b>
            <div>
                {diff}
            </div>
            <br/>
            """

    return (has_change, diff_log)


async def generate_character_diff_log(base_version, alt_version) -> (bool, str):

    character_pairs = {}

    async for character in base_version.character.all():
        character_pairs[character.app_id] = {"base": character}

    async for character in alt_version.character.all():
        character_pair = character_pairs.get(character.app_id, {})
        character_pair["alt"] = character
        character_pairs[character.app_id] = character_pair

    hash_change = False
    diff_log = ""

    for pair in character_pairs.values():
        base = pair.get("base")
        alt = pair.get("alt")

        if base is None and alt is not None:
            has_change = True
            diff_log += dedent(f"""
            <b>Character Added: {alt.alias}({alt.name})</b>
            <br/>
            """).strip() + "\n\n"
        elif base is not None and alt is None:
            has_change = True
            diff_log += dedent(f"""
            <b>Character Removed: {base.alias}({base.name})</b>
            <br/>
            """).strip() + "\n\n"
        elif base is not None and base is not None:
            has_change = True

            character_has_change, character_diff_log = await compare_characters(base, alt, base_version, alt_version)

            hash_change = hash_change or character_has_change
            if character_has_change:
                diff_log += character_diff_log


    return (has_change, diff_log)


async def compare_characters(base, alt, base_version, alt_version):
    # compare affiliations
    affiliation_pair = {}

    has_change = False

    if base is not None:
        name = base.name
        alias = base.alias
    elif alt is not None:
        name = alt.name
        alias = alt.alias
    diff_log = f"""
    <h4>Character Modified: {alias} ({name})</h4>
    """


    for affiliation in base.affiliations:
        affiliation_pair[affiliation["affiliation_id"]] = {"base": affiliation}

    for affiliation in alt.affiliations:
        if affiliation["affiliation_id"] in affiliation_pair:
            pair = affiliation_pair[affiliation["affiliation_id"]]
        else:
            pair = {}
        pair["alt"] = affiliation
        affiliation_pair[affiliation["affiliation_id"]] = pair

    for pair in affiliation_pair.values():
        base_aff = pair.get("base")
        alt_aff = pair.get("alt")

        if base_aff is None and alt_aff is not None:
            has_change = True
            affiliation_entity = await alt_version.affiliation.filter(app_id=alt_aff["affiliation_id"]).first()
            diff_log += f"""
            <div><b>Character Affiliation Added:</b> {affiliation_entity.name}</div>
            """
        elif base_aff is not None and alt_aff is None:
            has_change = True
            affiliation_entity = await base_version.affiliation.filter(app_id=base_aff["affiliation_id"]).first()
            diff_log += f"""
            <div><b>Character Affiliation Removed:</b> {affiliation_entity.name}</div>
            """
        elif base_aff is not None and alt_aff is not None:

            for field in ["can_be_team_boss", "always_team_boss"]:
                if base_aff[field] and not alt_aff[field]:
                    has_change = True
                    diff_log += f"""
                    <div><b>Character Affiliation Modified:</b> {field} is False</div>
                    <br/>
                    """
                elif not base_aff[field] and alt_aff[field]:
                    has_change = True
                    diff_log += f"""
                    <div><b>Character Affiliation Modified:</b> {field} is True</div>
                    <br/>
                    """

            aff_rank_pairs = {}

            for aff_rank in base_aff["rank_ids"]:
                aff_rank_pairs[aff_rank] = {"base": True}
            for aff_rank in alt_aff["rank_ids"]:
                if aff_rank in aff_rank_pairs:
                    pair = aff_rank_pairs[aff_rank]
                else:
                    pair = {}
                pair["alt"] = True
                aff_rank_pairs[aff_rank] = pair

            for id, pair in aff_rank_pairs.items():
                rank_name = rank_id_to_name(id)
                base_aff_rank = pair.get("base", False)
                alt_aff_rank = pair.get("alt", False)

                if base_aff_rank and not alt_aff_rank:
                    has_change = True
                    diff_log += f"""
                    <div><b>Character Affiliation Rank Removed:</b> character can no longer be run as a {rank_name} in 
                    this affiliation.</div>
                    <br/>
                    """
                elif not base_aff_rank and alt_aff_rank:
                    has_change = True
                    diff_log += f"""
                    <div><b>Character Affiliation Rank Added:</b> character now be run as a {rank_name} in 
                    this affiliation.</div>
                    <br/>
                    """

    stats = [
        "willpower",
        "strength",
        "movement",
        "attack",
        "defense",
        "endurance",
        "reputation",
        "funding",
        "eternal",
        "bases_size",
        "shares_equipment",
        "can_be_taken_individually",
        "adds_to_model_count",
        "adds_to_rank_count"
    ]

    for stat in stats:
        base_stat = getattr(base, stat)
        alt_stat = getattr(alt, stat)

        pretty_stat = stat[0].upper() + stat[1:]

        if base_stat != alt_stat:
            has_change = True
            diff_log += f"""
            <div><b>{pretty_stat}:</b> {base_stat} -> {alt_stat} </div>
            <br/>
            """

    trait_pairs = {}

    for trait in base.traits:
        trait_pairs[trait["trait_id"]] = {"base": trait}

    for trait in alt.traits:
        if trait["trait_id"] in trait_pairs:
            pair = trait_pairs[trait["trait_id"]]
        else:
            pair = {}
        pair["alt"] = trait
        trait_pairs[trait["trait_id"]] = pair

    for pair in trait_pairs.values():
        base_trait = pair.get("base")
        alt_trait = pair.get("alt")

        if base_trait is None and alt_trait is not None:
            has_change = True
            trait = await alt_version.traits.filter(app_id=alt_trait["trait_id"]).first()
            diff_log += f"""
            <div><b>New Trait:</b> {trait.name} - {trait.description} </div>
            <br/>
            """

        if base_trait is not None and alt_trait is None:
            has_change = True
            trait = await base_version.traits.filter(app_id=base_trait["trait_id"]).first()
            diff_log += f"""
            <div><b>Removed Trait:</b> {trait.name} - {trait.description} </div>
            <br/>
            """

    weapon_pairs = {}

    for weapon_id in base.weapon_ids:
        weapon_pairs[weapon_id] = {"base": weapon_id}

    for weapon_id in alt.weapon_ids:
        if weapon_id in weapon_pairs:
            pair = weapon_pairs[weapon_id]
        else:
            pair = {}
        pair["alt"] = weapon_id
        weapon_pairs[weapon_id] = pair

    for pair in weapon_pairs.values():
        base_weapon = pair.get("base")
        alt_weapon = pair.get("alt")

        if base_weapon is not None and alt_weapon is None:
            has_change = True
            weapon = await base_version.weapon.filter(app_id=base_weapon).first()
            diff_log += f"""
            <div><b>Weapon Removed:</b> {weapon.name}</b></div>
            """
        elif base_weapon is None and alt_weapon is not None:
            has_change = True
            weapon = await alt_version.weapon.filter(app_id=alt_weapon).first()
            diff_log += f"""
            <div><b>Weapon Added:</b> {weapon.name}</b></div>
            """



    return (has_change, diff_log)


async def generate_weapon_diff_log(base_version, alt_version):
    weapon_pairs = {}
    diff_log = ""
    has_change = False

    # fetch base weapons
    for weapon in base_version.weapon:
        weapon_pairs[weapon.app_id] = {"base": weapon}

    # fetch alt weapons
    for weapon in alt_version.weapon:
        if weapon.app_id in weapon_pairs:
            pair = weapon_pairs[weapon.app_id]
        else:
            pair = {}
        pair["alt"] = weapon
        weapon_pairs[weapon.app_id] = pair

    # check if there are diffs
    for pair in weapon_pairs.values():
        base_weapon = pair.get("base")
        alt_weapon = pair.get("alt")

        if base_weapon is not None and alt_weapon is None:
            has_change = True
            diff_log += f"""
            <div><b>Weapon Removed:</b> {base_weapon.name}</b></div>
            """
        elif base_weapon is None and alt_weapon is not None:
            has_change = True
            diff_log += f"""
            <div><b>Weapon Added:</b> {alt_weapon.name}</b></div>
            """
        elif base_weapon is not None and alt_weapon is not None:
            # confirm if the profiles have changed.
            rate_of_fire_updated = base_weapon.rate_of_fire != alt_weapon.rate_of_fire
            ammunition_updated = base_weapon.ammunition != alt_weapon.ammunition
            if base_weapon.damage is not None:
                base_damage = "".join(transform_damage(d) for d in base_weapon.damage)
            else:
                base_damage  = "<no damage>"

            if base_weapon.damage is not None:
                alt_damage = "".join(transform_damage(d) for d in alt_weapon.damage)
            else:
                alt_damage = "<no damage>"

            damage_updated = base_damage != alt_damage

            base_trait_names = []
            alt_trait_names = []
            base_trait_ids = map(lambda t: t["trait_id"], base_weapon.traits)
            alt_trait_ids = map(lambda t: t["trait_id"], alt_weapon.traits)

            for trait_id in base_trait_ids:
                trait = await base_version.traits.filter(app_id=trait_id).first()
                base_trait_names.append(trait.name)

            for trait_id in alt_trait_ids:
                trait = await alt_version.traits.filter(app_id=trait_id).first()
                alt_trait_names.append(trait.name)

            traits_updated = set(base_trait_ids) != set(alt_trait_ids)

            profile_updated = (
                rate_of_fire_updated or
                ammunition_updated or
                damage_updated or
                traits_updated
            )

            if profile_updated:
                has_change = True
                diff_log = f"""
                <div>
                    <div><b>Weapon Profile Updated: {base_weapon.name}</b></div>
                    <div>
                        <span>
                            {base_damage} | ROF: {base_weapon.rate_of_fire} | AMMO: {base_weapon.ammunition} | Traits: {base_trait_names.sort()}
                        </span>
                        <span>
                            changed to 
                        </span>
                        <span>
                            {alt_damage} | ROF: {alt_weapon.rate_of_fire} | AMMO: {alt_weapon.ammunition} | Traits: {alt_trait_names.sort()}
                        </span> 
                    </div>
                </div>
                <br/>
                """

    return (has_change, diff_log)


def rank_id_to_name(id):
    if id == 1:
        return "Boss"
    elif id == 2:
        return "Sidekick"
    elif id == 3:
        return "Free Agent"
    elif id == 5:
        return "Henchmen"

def transform_damage(damage):
    if damage["damage_type_id"] == 1:
        damage_type = "blood"
    else:
        damage_type = "stun"

    return f"{damage['count']} {damage_type}"



