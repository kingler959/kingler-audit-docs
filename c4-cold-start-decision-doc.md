# C4 cold-start progression audit

**Date:** 2026-07-10

**Status:** team decision doc — verified findings; decisions pending
**Scope:** fresh Character with only Starting Node #0 applied, current primary C4 faucet bundle, current `programs/main`, canonical `sage-editor/master`, and pending Crafting target PRs #180/#807.

**Interactive version:** https://kingler959.github.io/kingler-audit-docs/

Use the interactive page to record decisions and export Markdown or JSON. Responses remain in the reviewer’s browser until exported.

## Executive verdict

The earlier statement that “every career has a verified XP source, so cold-start works in ~14 minutes” is no longer a valid end-to-end conclusion.

| Career | Literal first action available? | Fresh-player route | Verdict |
|---|---:|---|---|
| Pilot | Yes | Fimbul Airbike + Fuel → subwarp | Available; Pilot Character XP now uses PR #803’s shared budget. |
| Data Runner | Yes | Airbike + 22 Repair Kits → Broad Spectrum scan | Available; PR #808 grants 52 flat XP, not ~520. |
| Mining | Yes | Airbike + Ammo + Food → mine the CSS asteroid | Available; Starting Node grants all cargo categories and runtime does not enforce drill/hardness tags here. |
| Crafting | Yes | Public starbase + crew + an open recipe | Available without Crafting Hab #26. Ten intended-open recipes have complete starter inputs. |
| Building | **No** | Must first unlock stake capacity, place stake, then finalize a building | Delayed behind another career’s progression. Stake placement itself grants zero Building XP. |
| Combat | **No deterministic route** | Requires typed ship damage and a valid target | Starter Airbike has zero typed damage; program rejects the attack. Primary bundle has no damage-bearing remedy. |

**Overall:** four of six careers have a deterministic first action. Building and Combat do not.

## Sources and baselines

### Current generated/runtime target

- `staratlasmeta/programs@main`, commit `e2db621f8`
- `cli/c4-cli/conf/universe.json`
- merged Pilot budget PR #803
- merged Data Runner/flat scan XP PR #808
- open Crafting anti-farm PR #807

### Canonical data target

- `staratlasmeta/sage-editor@master`, commit `d21010b`
- `SAGE Editor Suite/Research Nodes/research_nodes-careercombatspread.json`
- `SAGE Editor Suite/C4 Tools/data/level_thresholds.json`
- open Crafting SoT PR #180

### Starter bundle

- `staratlasmeta/zink-web@main`, commit `e9d7947`
- `packages/zink-profile-api/src/constants/c4-starter-bundle.constants.ts`
- `star-atlas-tech/packages/fc-app/src/providers/OnboardingFaucetProvider.tsx`

The primary starter bundle contains 44 token entries plus 10 SOL and a 1,000-ATLAS target. The onboarding client separately auto-claims 1,000 crew once the CSS `StarbasePlayer` exists.

HYE adds two extra combat stimulants in its variant. They are not part of the primary bundle pasted for this audit.

## 1. Starting Node #0

Canonical SoT #0 grants:

```json
{
  "cargo_categories": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
  "fleet_size": 4,
  "fleet_concurrency": 5,
  "max_ship_size": "XxSmall",
  "research_tags": [0]
}
```

It does **not** grant:

- `max_productive_plot_tier`
- `max_productive_plots`
- `max_residential_plot_tier`
- `max_residential_plots`
- typed combat damage

Consequences:

- Fimbul Airbike is usable immediately.
- Larger starter ships remain unusable until ship-size progression.
- No Claim Stake or Crafting Hab can be placed from Starting Node alone.
- Public starbase crafting remains available for recipes that do not require a hab.

## 2. Claim Stake and Crafting Hab gate divergence

### Canonical sage-editor SoT

```text
#0 Starting Node
  └─ #45 Council Rank       cost: 1 CouncilRank XP
       ├─ #21 Claim Stake T1   cost: 1 CouncilRank XP
       └─ #26 Crafting Hab T1  cost: 1 CouncilRank XP
```

Therefore:

- T1 Claim Stake access costs **2 renown**.
- T1 Crafting Hab access costs **2 renown**.
- 6 feeder-career levels = 1 renown.
- Either access path requires **12 levels from other careers**.

The user’s “at least six levels” statement is correct for current `programs/main`, but not for canonical SoT.

### Current programs/main generated config

```text
#45 Council Rank: absent
#21 Claim Stake T1: roots on #0
  cost: 1 CouncilRank XP + 1 DailyCheckIn XP
#26 Crafting Hab T1: roots on #0
  cost: 1 CouncilRank XP + 1 DailyCheckIn XP
```

Current generated behavior therefore needs:

- 6 feeder levels,
- one Daily XP,
- one ATLAS for the node.

This is a concrete generated-output/SoT divergence. The coordinated regen will change cold-start behavior unless the team decides which shape is intended.

## 3. Crafting: what is actually available

### No personal Crafting Hab is required for basic recipes

`start_crafting_process.rs` makes `crafting_hab_instance` optional. When it is omitted, the instruction only rejects recipes with `hab_required: true`.

Current `programs/main` has:

- 3,150 recipes,
- 3,150 with empty `research_requirements`,
- 3,150 with `hab_building_required: false`.

PR #807 intends to gate value 30+ recipes and family recipes while leaving value 10–20 basics open.

### Copper versus Copper Ore

The starter bundle contains:

```text
Cargo #1033 Copper: 25,000
```

It does **not** contain:

```text
Cargo #311 Copper Ore
```

The recipes are:

```text
#37 Copper:
  input: 1 Copper Ore
  output: 1 Copper

#0 Ammunition:
  input: 2 Copper
  output: 1 Ammunition
  value: 20
  current duration/minimum: 1 second
  PR #807 duration/minimum: 80 seconds
  research requirements: []
  hab required: false
```

So the fresh player cannot initially craft Copper, but does not need to. The bundle already provides processed Copper for Ammunition and Copper Wire.

### Intended-open recipes with complete starter inputs

These ten value-10/20 recipes are buildable from the bundle and remain in PR #807’s intended open tier:

| Recipe | Value | Starter inputs |
|---|---:|---|
| Ammunition | 20 | 2 Copper |
| Fuel | 10 | 3 Hydrogen |
| Repair Kit | 20 | 2 Iron |
| Copper Wire | 10 | 1 Copper |
| Electromagnet | 20 | 4 Copper Wire + 1 Magnet |
| Electronics | 10 | 1 Copper + 1 Polymer |
| Framework | 10 | 2 Iron |
| Heat Distribution Grid | 10 | 1 Copper + 2 Iron |
| Magnet | 20 | 2 Iron |
| Polymer | 10 | 1 Hydrocarbon |

Current ungated config has 16 total bundle-compatible recipes; the six value-30/40/50 recipes should become gated in the intended rework.

### Recipe SoT blocker

PR #180 explicitly records that `research_requirements`, `value`, and `crafting_duration` have no durable recipe SoT home today. They are either passed through from the chosen live baseline or defaulted for newly emitted recipes.

Therefore the team cannot claim the post-regen starter recipe contract is guaranteed until the recipe SoT/converter seam lands.

Required deployment assertion:

```text
Ammunition #0 must emit with:
- value = 20
- input #1033 Copper ×2
- research_requirements = []
- hab_required = false
- intended duration/minimum
```

## 4. Crafting pacing defect

### Current programs/main

Current completion XP is:

```rust
recipe.value × crafting_process.quantity
```

Current Crafting curve reaches L6 at 500 XP. A fresh player can:

- start Ammunition quantity 25,
- assign 25 of the 1,000 faucet crew,
- complete in one second because duration = `max(1, 1×25/25)`,
- receive 20×25 = 500 Crafting XP,
- reach Crafting L6 and produce one renown.

This directly satisfies the current #21 renown gate.

### PRs #807/#180 target

PR #807 changes XP to flat `recipe.value` per completed process and pegs minimum duration to `value × 4`. PR #180’s proposed Crafting curve reaches:

- L6 at 529 XP,
- L12 at 1,499 XP.

A value-20 process therefore needs:

- 27 separate processes for L6,
- 75 separate processes for L12 / two renown.

However, the public no-hab path does not call `CraftingHabInstance::try_add_job`. `StarbasePlayer` has crew allocation but no public crafting-process concurrency field. The Ammunition recipe has a global usage limit of 100.

A fresh player with 1,000 crew can therefore launch 75 one-crew Ammunition processes, wait 80 seconds, and earn two renown. Inputs and fees:

- 150 Copper out of 25,000,
- 75 crew out of 1,000,
- 75,000 raw ATLAS units = 0.00075 ATLAS.

PR #807 removes the batch multiplier but leaves per-process parallelism as the dominant XP strategy.

**Recommendation:** do not use recipe-global `usage_limit` as the fix; it is shared by all players and can be bypassed with multiple basic recipes. Add either:

1. a per-Character public-station process cap, or
2. a shared Character Crafting XP time budget/diminished tail.

## 5. Building bootstrap

### What awards Building XP

Claim Stake placement itself gives zero Building XP.

`finalize_building_changes.rs` grants:

```rust
building_def.xp_value × positive change_amount
```

Removing buildings grants no XP. Passive claim-stake production and cargo collection grant no career XP.

### Starter bundle material coverage

Current config has 404 T1 building definitions. Exactly:

```text
0 / 404 T1 buildings are directly constructible from starter-bundle cargo.
```

A T1 stake’s matching Central Hub is the first practical building. Examples:

| Hub | Missing starter inputs | Existing processed input |
|---|---|---|
| Oceanic | 25 Chromite Ore + 15 Copper Ore | 20 Copper |
| Terrestrial | 25 Arco + 15 Copper Ore | 20 Framework |
| Asteroid | 25 Carbon + 20 Copper Ore + 15 Iron Ore | — |
| Ice Giant | 25 Chromite Ore + 20 Lumanite | 15 Hydrogen |

The MUD CSS asteroid contains the missing inputs for seven of the eight hub archetypes. The Volcanic hub additionally needs processed Neodymium, so a player should choose another available planet unless that processing chain is completed.

The simplest MUD route is a Terrestrial hub:

```text
mine 25 Arco + 15 Copper Ore
use 20 starter Framework
finalize Terrestrial Central Hub T1
receive 100 Building XP
```

At one Airbike’s 0.262-unit/sec total rate, the 40 missing units have an ideal production floor of about 153 seconds; five Airbikes reduce the aggregate production floor to about 31 seconds before loading, travel, resource splitting, and transactions.

Building XP is awarded during finalization before the 90-second construction timer completes. The 100 XP reaches Building L2 on the canonical shared curve, enough to unlock Freelance Builder #64.

### Building verdict

This is not an absolute resource deadlock, but Building is **not a literal cold-start career**. It depends on:

1. another career producing renown,
2. the Council Rank/stake gate,
3. Mining the hub inputs,
4. placing a stake,
5. finalizing the hub.

If design intent says every career can begin from Starting Node, current data violates that intent.

## 6. Other first actions

### Pilot

Available:

- Starting Node permits XxSmall.
- Bundle provides 34 Fimbul Airbikes and 250,000 Fuel.
- Airbike default `subwarp_xp_rate = 1`.
- PR #803 caps Character Pilot XP through a shared regenerating budget.

### Data Runner

Available:

- Airbike default cooldown: 786 seconds.
- Airbike scan cost: 22.
- Broad Spectrum cost cargo: #3 Repair Kit.
- Bundle provides 10,000 Repair Kits, enough for 454 scans.
- Broad Spectrum grants 52 flat Data Runner XP whether loot or blank.
- Survey Data Units #366 are scan output in this configuration, not the scan input.

On the canonical shared curve:

- one scan → Data Runner L1,
- five scans → L3,
- thirteen scans → L6.

Five fleets can perform five scans per 13.1-minute cooldown wave, but this is not the fastest renown source.

### Mining

Available:

- Airbike mining rate: 0.262 units/sec.
- Bundle provides Ammo and Food.
- CSS has an asteroid containing the T1 hub ores.
- `start_mining_asteroid` verifies resource presence and cargo-category permission.
- Starting Node grants every cargo category.
- Current instruction does not enforce the Mining drill/hardness research tags.

Five one-Airbike fleets reach Mining L6’s 674-XP threshold in an ideal ~8.6 minutes before logistics.

### Combat

Not deterministically available:

- Airbike default config has HP/SP/AP but no nonzero typed damage field.
- No ship config in current generated `universe.json` emits a typed damage field.
- Combat V2 calls `ensure_combat_v2_damage` and rejects zero-damage attackers.
- Primary starter bundle has no weapon-bearing config/token.
- A valid hostile/tutorial target is not guaranteed.

The Rust/config schema and converter support typed damage fields, so authoring a small starter `damage_kinetic` value is data-capable. A valid training target remains a separate requirement.

## 7. First-hours models

### Current programs/main behavior

Fastest observed gate route:

1. Onboarding claims starter cargo, 1,000 ATLAS, and 1,000 crew.
2. Daily check-in supplies the Daily XP required by current #21.
3. Start Ammunition quantity 25 with 25 crew.
4. Complete after one second → 500 Crafting XP → L6 → one renown.
5. Buy #21 directly from #0.
6. Mine hub inputs, place stake, finalize hub → Building XP.

This is substantially faster than the prior ~14-minute model and is dominated by the current Crafting batch-XP farm.

### Canonical SoT + PRs #180/#807

Fastest observed gate route:

1. Start 75 separate one-crew Ammunition processes at the public starbase.
2. Wait 80 seconds.
3. Complete them → 1,500 Crafting XP → L12 → two renown.
4. Buy #45 and #21.
5. Mine hub inputs, place stake, finalize hub → Building XP.

A less transaction-heavy mixed route is:

- 27 parallel Ammunition processes → Crafting L6,
- five Airbikes mine to Mining L6 in ~8.6 ideal minutes,
- total 12 feeder levels → two renown.

The canonical gate is stricter, but public Crafting parallelism still makes the optimal path a transaction fan-out.

## 8. Recommended decisions and fixes

### P0 — decide the authoritative T1 stake/hab gate

Choose explicitly between:

- **Current generated shape:** #21/#26 root on #0, cost one renown + Daily XP.
- **Canonical SoT shape:** #45 then #21/#26, cost two renown, no Daily XP.
- **Immediate-career shape:** Starting Node grants one T1 stake/hab slot.

Do not let converter merge order decide this.

### P0 — guarantee one Building action from the starter contract

If Building must be available immediately, recommended data-only approach:

```json
Starting Node CVC:
{
  "max_productive_plot_tier": "1",
  "max_productive_plots": 1
}
```

Then preserve the intended post-#21 cap by changing #21 from `+20` to `+19`, or explicitly accept 21 total.

Also provide a T1 hub kit. Two options:

1. **Tutorial-specific:** guarantee a Terrestrial plot and add 25 Arco + 15 Copper Ore.
2. **Archetype-independent:** add enough missing raw inputs for any T1 hub:
   - Arco #302 ×25
   - Carbon #308 ×25
   - Chromite Ore #309 ×25
   - Copper Ore #311 ×20
   - Iron Ore #329 ×20
   - Lumanite #334 ×20
   - Rhenium Ore #355 ×20
   - Neodymium #1171 ×15

The second option is robust but larger. The first is cleaner if onboarding can guarantee the plot archetype.

### P0 — close the recipe SoT seam

Before canonical regen, add `research_requirements`, `value`, `crafting_duration`, and the relevant hab/minimum fields to recipe SoT/converter ownership. Add a test asserting Ammunition remains open and bundle-compatible.

### P0 — make Combat executable or stop claiming six-career bootstrap

Data-capable minimum:

- author nonzero typed damage on a starter XxSmall config,
- provide a guaranteed legal training target,
- verify one attack causes positive damage and Combat XP without destroying the onboarding fleet.

If this will not ship, documentation must say Combat is intentionally deferred.

### P1 — cap public Crafting progression, not public output

PR #807’s flat-per-process XP is necessary but insufficient. Add a per-Character limit or XP budget to prevent process fan-out. Preserve output scaling and better-crew value separately.

### P1 — correct onboarding copy

Surface these exact facts in the UI:

- Copper is provided; Copper Ore is not.
- Ammunition is the canonical first craft.
- Scans consume 22 Repair Kits with the starter Airbike.
- Building begins only after the configured stake gate and hub material sequence.
- Only the Fimbul Airbike is usable initially.

### P1 — add an executable cross-repo cold-start contract

At minimum assert:

- Starting Node grants the intended immediate capacities.
- Starter ship is usable and has the required action stats.
- At least one open recipe’s complete inputs are in the bundle.
- One T1 building is constructible from the guaranteed starter/tutorial inventory.
- Claim Stake/Crafting Hab gate shape matches the approved decision.
- Recipe regen does not drop value/duration/gates.
- Combat has positive typed damage and a target if advertised as bootstrappable.

## Reproducibility

Executable audit source: [`c4-cold-start-audit.py`](./c4-cold-start-audit.py)

```bash
python c4-cold-start-audit.py
```

Verified output:

```text
C4 COLD-START CONTRACT: PASS
primary bundle tokens: 44
Copper present: 25,000; Copper Ore absent
canonical stake gate: #0 -> #45 (1 renown) -> #21 (1 renown) = 2 renown / 12 feeder levels
programs-main stake gate: #0 -> #21 (1 renown + 1 Daily XP) = 1 renown / 6 feeder levels
bundle-compatible current recipes: 16; intended-open value<=20: 10
T1 buildings buildable directly from bundle: 0 / 404
T1 hub archetypes whose missing inputs exist on MUD CSS asteroid: 7 / 8
Fimbul Airbike: mining=yes, scanning=yes, typed combat damage=no
current programs one-renown Ammo batch: quantity 25
PR180/807 two-renown public-crafting route: 75 separate value-20 processes
```
