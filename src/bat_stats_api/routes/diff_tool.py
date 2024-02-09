from textwrap import dedent
from datetime import datetime

from aiohttp import web
from typing import NamedTuple
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

    base_version = await GameDataVersionEntity.filter(id=base_version_id).first()
    alt_version = await GameDataVersionEntity.filter(id=alt_version_id).first()

    if base_version is None:
       raise Exception(f"unable to find base version: {base_version}")

    if alt_version is None:
        raise Exception(f"unable to find alt version: {alt_version}")


    traits_changed, trait_change_log = await generate_trait_diff_log(base_version, alt_version)

    diff_log = trait_change_log
    has_change = traits_changed

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

    diff_log = ""
    has_change = False

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
