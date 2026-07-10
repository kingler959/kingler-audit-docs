#!/usr/bin/env python3
"""C4 cold-start contract audit against fetched repository snapshots.

Expected inputs are refreshed from Git before running:
  /tmp/programs-main-universe-coldstart.json
  /tmp/cold-sot-master.json
  /tmp/cold-sot-crafting.json
  /tmp/cold-level-master.json
  /tmp/cold-level-pr180.json
  /tmp/cold-bundle-current.ts
"""

from __future__ import annotations

import bisect
import json
import math
import re
from pathlib import Path

PROGRAMS = Path("/tmp/programs-main-universe-coldstart.json")
SOT_MASTER = Path("/tmp/cold-sot-master.json")
SOT_CRAFTING = Path("/tmp/cold-sot-crafting.json")
LEVEL_MASTER = Path("/tmp/cold-level-master.json")
LEVEL_PR180 = Path("/tmp/cold-level-pr180.json")
BUNDLE_TS = Path("/tmp/cold-bundle-current.ts")


def load(path: Path):
    return json.loads(path.read_text())


def parse_primary_bundle(path: Path):
    text = path.read_text()
    start = text.index("export const C4_STARTER_BUNDLE_TOKENS")
    end = text.index("\n];", start)
    block = text[start:end]
    tokens = []
    for obj in re.findall(r"\{(.*?)\n  \}", block, flags=re.S):
        def field(name: str):
            match = re.search(rf"\b{name}:\s*(?:'([^']*)'|([\d_]+))", obj)
            if not match:
                return None
            return match.group(1) if match.group(1) is not None else int(match.group(2).replace("_", ""))

        category = field("category")
        token_id = field("id")
        name = field("name")
        quantity = field("quantity")
        if category and token_id is not None:
            tokens.append({"category": category, "id": token_id, "name": name, "quantity": quantity})
    return tokens


def node_map(doc):
    return {
        int(node["c4_numerical_id"]): node
        for node in doc["nodes"]
        if isinstance(node.get("c4_numerical_id"), int)
    }


def level_for(thresholds, xp):
    return bisect.bisect_right(thresholds, xp)


def main():
    universe = load(PROGRAMS)
    sot = node_map(load(SOT_MASTER))
    sot_crafting = node_map(load(SOT_CRAFTING))
    master_levels = load(LEVEL_MASTER)["thresholds"]
    pr180_levels = load(LEVEL_PR180)["thresholds"]
    bundle = parse_primary_bundle(BUNDLE_TS)
    bundle_by_id = {entry["id"]: entry for entry in bundle}
    starter_ids = set(bundle_by_id)

    # Bundle identity.
    assert bundle_by_id[1033]["name"] == "Copper"
    assert 311 not in starter_ids, "Copper Ore unexpectedly present; update the report"
    assert bundle_by_id[1033]["quantity"] == 25_000

    # Canonical SoT gate shape.
    assert sot[0]["character_value_changes"]["max_ship_size"] == "XxSmall"
    assert "max_productive_plot_tier" not in sot[0]["character_value_changes"]
    assert "max_residential_plot_tier" not in sot[0]["character_value_changes"]
    assert sot[45]["requirements"]["required_tags"] == [0]
    assert sot[45]["cost"]["xp_cost"] == {"CouncilRank": 1}
    assert sot[21]["requirements"]["required_tags"] == [45]
    assert sot[21]["cost"]["xp_cost"] == {"CouncilRank": 1}
    assert sot[26]["requirements"]["required_tags"] == [45]
    assert sot[26]["cost"]["xp_cost"] == {"CouncilRank": 1}

    # Current programs-main divergence.
    live_nodes = {int(k): v for k, v in universe["research_nodes"].items()}
    assert 45 not in live_nodes
    assert live_nodes[21]["requirements"]["required_tags"] == [0]
    assert live_nodes[21]["cost"]["xp_cost"] == {"CouncilRank": 1, "DailyCheckIn": 1}

    # Recipe availability and starter compatibility.
    recipes = universe["recipes"]
    ammo = recipes["0"]
    assert ammo["name"] == "Ammunition"
    assert ammo["inputs"] == {"1033": 2}
    assert ammo["research_requirements"] == []
    assert ammo["hab_building_required"] is False
    assert ammo["value"] == 20
    assert ammo["usage_limit"] == 100
    assert all(not recipe["research_requirements"] for recipe in recipes.values())
    assert all(not recipe["hab_building_required"] for recipe in recipes.values())

    compatible = []
    for recipe_id, recipe in recipes.items():
        inputs = {int(k): int(v) for k, v in recipe["inputs"].items() if int(v) > 0}
        if inputs and set(inputs) <= starter_ids and not recipe["research_requirements"] and not recipe["hab_building_required"]:
            compatible.append((int(recipe_id), recipe))
    intended_open = [(recipe_id, recipe) for recipe_id, recipe in compatible if recipe["value"] <= 20]
    assert len(compatible) == 16
    assert len(intended_open) == 10

    # Building bootstrap materials.
    buildings = universe["claim_stake_values"]["buildings"]
    tier_one = [building for building in buildings.values() if building["min_tier"] == "1"]
    bundle_buildable = [
        building
        for building in tier_one
        if set(map(int, building["construction_cost"])) <= starter_ids
    ]
    assert len(tier_one) == 404
    assert not bundle_buildable

    hubs = [building for building in tier_one if "Central Hub Tier 1" in building["name"]]
    assert len(hubs) == 8
    css_asteroid_ids = set(map(int, universe["map"]["systems"]["0"]["asteroids"][0]["resources"]))
    mineable_hubs = []
    for hub in hubs:
        missing = set(map(int, hub["construction_cost"])) - starter_ids
        if missing <= css_asteroid_ids:
            mineable_hubs.append(hub)
    assert len(mineable_hubs) >= 1

    # Starter ship capabilities.
    airbike = universe["ships"]["map"]["1"]["configs"]["101"]["stats"]
    assert airbike["ship_size"] == "XxSmall"
    assert airbike["asteroid_mining_rate"] == 0.262
    assert airbike["scan_cool_down"] == 786
    assert airbike["scan_cost"] == 22
    damage_fields = [
        "damage_kinetic", "damage_energy", "damage_emp", "damage_superchill",
        "damage_shockwave", "damage_graygoo", "damage_heat", "damage_bomb", "missile_damage",
    ]
    assert not any(float(airbike.get(field, 0)) > 0 for field in damage_fields)

    # Progression snapshots.
    master_crafting = master_levels["crafting"]["levels"]
    pr180_crafting = pr180_levels["crafting"]["levels"]
    assert master_crafting[5] == 674 and master_crafting[11] == 2435
    assert pr180_crafting[5] == 529 and pr180_crafting[11] == 1499
    pr180_jobs_for_two_renown = math.ceil(pr180_crafting[11] / 20)
    assert pr180_jobs_for_two_renown == 75
    assert level_for(pr180_crafting, pr180_jobs_for_two_renown * 20) == 12

    current_crafting = universe["level_thresholds"]["crafting"]
    current_batch_qty_for_one_renown = math.ceil(current_crafting[5] / ammo["value"])
    assert current_batch_qty_for_one_renown == 25

    print("C4 COLD-START CONTRACT: PASS")
    print(f"primary bundle tokens: {len(bundle)}")
    print("Copper present: 25,000; Copper Ore absent")
    print("canonical stake gate: #0 -> #45 (1 renown) -> #21 (1 renown) = 2 renown / 12 feeder levels")
    print("programs-main stake gate: #0 -> #21 (1 renown + 1 Daily XP) = 1 renown / 6 feeder levels")
    print(f"bundle-compatible current recipes: {len(compatible)}; intended-open value<=20: {len(intended_open)}")
    print(f"T1 buildings buildable directly from bundle: {len(bundle_buildable)} / {len(tier_one)}")
    print(f"T1 hub archetypes whose missing inputs exist on MUD CSS asteroid: {len(mineable_hubs)} / {len(hubs)}")
    print("Fimbul Airbike: mining=yes, scanning=yes, typed combat damage=no")
    print(f"current programs one-renown Ammo batch: quantity {current_batch_qty_for_one_renown}")
    print(f"PR180/807 two-renown public-crafting route: {pr180_jobs_for_two_renown} separate value-20 processes")


if __name__ == "__main__":
    main()
