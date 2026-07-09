# C4 Mining & Building Trees — Verified Structure + Proposed Changes

**Star Atlas · C4 Progression**
**Date:** 2026-07-09
**Author:** Kingler (AI) for Joseph Floyd
**Status:** For team approval — no data changes made yet
**Audience:** Xcode, ZeSKK, bravetarget, bunthius, Jacob

---

## How to respond

This doc proposes specific node-level changes to the Mining and Building research trees. **No data has been changed.** Each change is scoped so you can approve/reject individually.

1. Open the rendered doc: https://kingler959.github.io/kingler-audit-docs/c4-mining-building-verified-trees.html
2. Review the current tree structure (verified against SoT) and the proposed changes
3. For each proposed change, pick Approve / Reject / Modify in the decision form
4. Click **Export** → choose Markdown or JSON
5. Send the file back to Joseph

---

## 1. Why this doc exists

The earlier `MINING-BUILDING-TREE-REDESIGN-PROPOSAL.md` (2026-07-08) contained several **factual errors** when cross-referenced against the actual SoT data (`research_nodes-careercombatspread.json`):

| Claim in original proposal | Reality (verified) |
|---|---|
| "Remove #83, #124, #125, #126 Regional Extraction branch" | ✅ **Correct** — all 4 nodes have zero buildings gated by their tags (dead). |
| "Remove #117 Siphon Drill" | ✅ **Correct** — tag 117 has zero building references. |
| "#82 Rare Mineral Discoveries — empty CVC" | ✅ **Correct** — `rare_mineral_discovery: {}` confirmed empty. |
| "Add #377 Deep Vein Extraction (new)" | ✅ **Correct** — #377 is available. |
| "Add #378 Industrial Throughput (new)" | ✅ **Correct** — #378 is available. |
| "#86 Construction Conditionals — spine (WIRED UP)" | ❌ **WRONG** — `Construction Conditionals` exists but has **no c4_numerical_id assigned** and is `c4_status: v2`. It cannot be referenced as "#86" because no node has that ID. |
| "#137 Master Construction (endless)" | ❌ **WRONG** — #137 is currently **`Advanced Crafting`** in the **Crafting** career. Repurposing it for Building would delete an active Crafting node. |
| "#136a Medium Risk Construction" | ❌ **WRONG** — #136 is **`Complex Crafting`** in the Crafting career. ID collision. |
| "Mining: 27 → 25 nodes" | ⚠️ **Miscounted** — Mining has 26 v1 nodes (not 27), minus 5 removals = 21, plus #377 = 22. |
| "Building: 19 → 24 nodes" (summary) vs "22 nodes" (heading) | ⚠️ **Internally contradictory.** |

**The mechanical fixes (dead-node removal, endless-node activation) are sound.** The ID assignments and counts need correction. This doc supersedes the original proposal and uses only verified IDs.

---

## 2. Current Mining tree — as it exists today

**Source:** `research_nodes-careercombatspread.json` (26 v1/v1-add nodes, 1 v2)

All costs uniform: 100M ATLAS, no XP cost, requires Mining L1. The structure is a hub-and-spoke off Freelance Miner with sequential tier ladders.

```
Starting Node (#0)
└── #62 Freelance Miner [requires tag 0, Mining L1]
    │
    ├── #79 Mining Drill & Laser Types [spine]
    │   ├── #111 Ore Breaker          (common ores)
    │   ├── #112 Mineral Laser         (rare minerals)
    │   ├── #113 Gas Condenser         (atmospheric gases)
    │   ├── #114 Vapor Beam            (volatile compounds — only 5 buildings)
    │   ├── #115 Crystal Resonator     (energy crystals)
    │   ├── #116 Fluid Extraction      (organic fluids)
    │   ├── #117 Siphon Drill          ⚠ DEAD — 0 buildings gated by tag 117
    │   └── #118 Exotic Matter         (exotic resources)
    │
    ├── #80 Mining Drill & Laser Tiers [spine, sequential]
    │   └── #119 T1 → #120 T2 → #121 T3 → #122 T4 → #123 T5
    │
    ├── #81 Mining Hardness Access [spine, sequential]
    │   └── #156 Fragile → #157 Moderate → #158 Reinforced → #159 Ultra-Dense
    │
    ├── #82 Rare Mineral Discoveries [scalability: Unlimited]
    │   └── CVC: rare_mineral_discovery: {} (EMPTY — needs population to function)
    │
    └── #83 Regional Extraction Tiers [spine]
        ├── #124 Faction Region Extraction    ⚠ DEAD — tag 124 has 0 refs
        ├── #125 Enemy Faction Extraction     ⚠ DEAD — tag 125 has 0 refs
        │   (CVC: enemy_faction_zone_access: true)
        └── #126 Deep Space Extraction        ⚠ DEAD — tag 126 has 0 refs
            (CVC: security_zone_access: HighRiskZone)
```

**Observations:**
- 5 of 26 nodes are dead (tag nothing). All live under the Regional Extraction branch (#83 spine) except #117.
- #82 is marked Unlimited but has empty CVC — effectively a no-op node today.
- Every node costs 100M ATLAS and has no XP cost. Flat pricing.
- No endless node is actually functional (would need populated CVC + `max_level: 0` in the new schema).

---

## 3. Current Building tree — as it exists today

**Source:** same file (13 v1/v1-add nodes, 6 v2)

```
Starting Node (#0)
└── #64 Freelance Builder [requires tag 0, Building L1]
    │
    ├── #84 Structural Complexity Access [spine]
    │   └── #127 T1 → #128 T2 → #129 T3 → #130 T4 → #131 T5  (sequential)
    │
    ├── #85 Specialized Structure Unlocks [spine]
    │   ├── #132 MUD Faction Buildings
    │   ├── #133 ONI Faction Buildings
    │   └── #134 Ustur Faction Building
    │
    └── #87 Regional Construction Tiers [spine]
        └── #135 Medium Risk Building (CVC: security_zone_access: MediumRiskZone)

[6 v2 nodes — NOT in v1 scope:]
  • Certified Builder (no ID assigned)
  • Construction Conditionals (no ID assigned, Successive Range scalability)
  • Aquatic, Extreme Surfaces, Hostile Atmospheres, Exotic Conditions (no IDs)
```

**Observations:**
- Building is ~half the depth of Mining (13 v1 nodes vs 26).
- No endless node exists. No endless candidate was ever stubbed.
- All 3 v2 terrain conditionals (Aquatic, Extreme Surfaces, Hostile Atmospheres, Exotic Conditions) live under the `Construction Conditionals` spine — which itself has no ID assigned. This is why they're blocked from v1.
- #135 Medium Risk Building already has `security_zone_access: MediumRiskZone` CVC — it's functional, just buried under #87.

---

## 4. Proposed changes — Mining

### M1. Remove 5 dead nodes

**Approve to remove these nodes** (set `c4_status: "never"` or delete from SoT):

| ID | Name | Why remove |
|---|---|---|
| #117 | Siphon Drill | Tag 117 gates 0 buildings. Confirmed via `claimStakeBuildings.json` scan. |
| #83 | Regional Extraction Tiers (spine) | Tag 83 gates 0 buildings. Entire branch is dead. |
| #124 | Faction Region Extraction | Tag 124 gates 0 buildings. |
| #125 | Enemy Faction Extraction | Tag 125 gates 0 buildings. (CVC `enemy_faction_zone_access: true` was never wired to anything that reads it.) |
| #126 | Deep Space Extraction | Tag 126 gates 0 buildings. (CVC `security_zone_access: HighRiskZone` was never wired.) |

**Net effect:** Mining drops from 26 → 21 v1 nodes. No player-facing functionality lost — these nodes literally do nothing today.

**Risk:** If any player has already researched these nodes on dev, they'd lose the tag (but the tag granted nothing, so no real loss). Worth flagging to Jacob for migration safety.

### M2. Activate #82 Rare Mineral Discoveries as endless node

Currently `scalability: Unlimited` with empty `rare_mineral_discovery: {}` CVC. Activate by:

- Add `max_level: 0` and `cost_growth_bps: 1000` (uses the new converter schema)
- Populate `rare_mineral_discovery` with T3+ rare mineral cargo IDs (proposal suggests ×1.05 multiplier per level per cargo)
- Add XP cost: `Mining: { minimum_level: 5, cost: 500 }` (prestige gate)

**Player fantasy:** "Each level boosts rare mineral yield by 5% multiplicatively. L10 = ×1.63, L20 = ×2.65."

### M3. Add #377 Deep Vein Extraction (new endless node)

- `c4_numerical_id: 377` (available)
- `max_level: 0`, `cost_growth_bps: 500` (gentler curve — common ore track)
- CVC: `rare_mineral_discovery` with T1-T2 common ores at ×1.03/level
- XP cost: `Mining: { minimum_level: 3, cost: 250 }` (accessible track)
- Requires tag 62 (off Freelance Miner)

**Player fantasy:** "Volume track for common-ore miners. L10 = ×1.34, L20 = ×1.81."

### M4. (Optional) Vapor Beam coverage check

#114 Vapor Beam only gates 5 buildings (fewest of any drill-type node). Either:
- **A.** Expand its resource coverage in `claimStakeBuildings.json` to cover more volatile-compound resources
- **B.** Leave as-is — 5 buildings is thin but functional
- **C.** Fold #114 into #113 Gas Condenser (merge tags)

**Recommend B for Monday** — revisit post-launch when resource coverage is tuned.

---

## 5. Proposed changes — Building

### B1. Activate Construction Conditionals + assign ID

The `Construction Conditionals` node exists in the SoT as `c4_status: v2` with **no `c4_numerical_id` assigned**. To activate:

- Assign a new ID (e.g., #379 — available, keeps endless-node IDs 377/378 clean)
- Flip `c4_status: v2 → v1-add`
- This becomes the spine for the 4 terrain conditionals

**This is required** before B2/B3 below can ship — the terrain conditionals need a parent spine.

### B2. Flip 4 terrain conditionals to v1

Currently `c4_status: v2` with no IDs. Assign IDs and flip to `v1-add`:

| Proposed ID | Name | Gates |
|---|---|---|
| #380 | Aquatic | Oceanic planet construction |
| #381 | Extreme Surfaces | Gas/Ice Giant planet construction |
| #382 | Hostile Atmospheres | Volcanic planet construction |
| #383 | Exotic Conditions | Dark planet construction |

**All require** the Construction Conditionals spine (#379) as prerequisite.

**Risk:** These gate planet-archetype building placement. Need to verify `planetArchetypes.json` actually has risk tiers that these tags can gate. **This needs design confirmation before data work.**

### B3. Move #135 Medium Risk Building under Construction Conditionals

Currently under #87 Regional Construction Tiers. Move to require #379 (Construction Conditionals) instead. This is a logical re-homing — #135 grants `security_zone_access: MediumRiskZone` which fits the terrain/conditions theme better than the regional tiers theme.

### B4. Remove #87 Regional Construction Tiers (spine)

After B3 moves #135 out, #87 has no children. It becomes a hollow spine. Remove it (set `c4_status: "never"`).

### B5. Add #378 Industrial Throughput (new endless node)

- `c4_numerical_id: 378` (available)
- `max_level: 0`, `cost_growth_bps: 1200`
- CVC: `crafting_efficiency_modifier: 0.01` (additive per level, capped at +1.0 total by engine)
- XP cost: `Building: { minimum_level: 3, cost: 300 }`
- Requires tag 64 (off Freelance Builder)

**Player fantasy:** "+1% processor efficiency per level. L10 = +10% output, L20 = +20%. Caps at +100% from all sources."

### B6. (Open question) Add Building slot endless node?

The original proposal suggested a second Building endless node for `max_productive_plots` / `max_residential_plots` (+1 slot per level). This would need a **new ID** (not #137 — that's Crafting's `Advanced Crafting`).

**Options:**
- **A.** Add it with a new ID (e.g., #384). Player fantasy: "+1 building slot per level."
- **B.** Skip for Monday — one endless node (#378) is enough for Building. Add slot-endless post-launch.
- **C.** Skip entirely — slot expansion feels like a Building-tier function, not a prestige track.

**Recommend B for Monday.** One endless track per career is enough to validate the pattern.

---

## 6. What about #137 Master Construction?

The original proposal named #137 as a Building endless node. **That was wrong.** #137 is `Advanced Crafting` in the Crafting career — an active, in-use node.

**Resolution:** Drop the #137 reference entirely. If we want a Building slot-endless node (see B6), use a new ID like #384. Do not touch #137.

---

## 7. ID assignment summary

**Currently assigned (verified):**
- Mining: 62, 79-83, 111-126, 156-159 (26 nodes)
- Building: 64, 84-85, 87, 127-135 (13 nodes)
- Max ID in use: 376

**Proposed new assignments:**

| ID | Career | Name | Status |
|---|---|---|---|
| #377 | Mining | Deep Vein Extraction (endless) | new |
| #378 | Building | Industrial Throughput (endless) | new |
| #379 | Building | Construction Conditionals (spine, was v2 no-ID) | activate |
| #380 | Building | Aquatic (was v2 no-ID) | activate |
| #381 | Building | Extreme Surfaces (was v2 no-ID) | activate |
| #382 | Building | Hostile Atmospheres (was v2 no-ID) | activate |
| #383 | Building | Exotic Conditions (was v2 no-ID) | activate |
| #384 | Building | (optional, B6) Slot Endless | new if approved |

**Proposed removals** (set `c4_status: "never"`):
- Mining: #83, #117, #124, #125, #126
- Building: #87

---

## 8. Node count math (corrected)

| Career | Current v1 | Removals | Activations (v2→v1) | New | Proposed v1 total |
|---|---|---|---|---|---|
| Mining | 26 | -5 | 0 | +1 (#377) | **22** |
| Building | 13 | -1 (#87) | +5 (#379-#383) | +1 (#378) + optional #384 | **19 or 20** |

---

## 9. Dependencies & sequencing

```
Phase 1 (zero-risk, ships Monday):
  M1 (remove 5 dead Mining nodes)
  M2 (activate #82 with populated CVC)
  M3 (add #377)
  B1 (assign #379 to Construction Conditionals, flip to v1)
  B3 (move #135 under #379)
  B4 (remove #87)
  B5 (add #378)
  + Converter schema PR (max_level + cost_growth_bps emit)

Phase 2 (needs design confirm):
  B2 (flip 4 terrain conditionals — needs planetArchetypes.json verification)

Phase 3 (optional):
  M4 (Vapor Beam coverage)
  B6 (Building slot endless #384)
```

**Phase 1 is self-contained** — no external dependencies, no design questions beyond endless-node curve tuning (which the handoff doc covers).

---

## 10. Decision Record

> **Workflow:** Fill in the interactive form on the [rendered HTML page](https://kingler959.github.io/kingler-audit-docs/c4-mining-building-verified-trees.html). Pick a verdict for each, add rationale, click Export, send the file back to Joseph.

| # | Change | Verdict | Rationale |
|---|---|---|---|
| M1 | Remove 5 dead Mining nodes (#83, #117, #124, #125, #126) | _pending_ | |
| M2 | Activate #82 Rare Minerals as endless (populate CVC + max_level:0) | _pending_ | |
| M3 | Add #377 Deep Vein Extraction (new endless, common ores) | _pending_ | |
| M4 | Vapor Beam coverage (A=expand / B=leave / C=merge) | _pending_ | |
| B1 | Assign #379 to Construction Conditionals, flip v2→v1 | _pending_ | |
| B2 | Flip 4 terrain conditionals to v1 (#380-#383) — needs planetArchetypes confirm | _pending_ | |
| B3 | Move #135 Medium Risk under #379 | _pending_ | |
| B4 | Remove #87 Regional Construction Tiers (hollow after B3) | _pending_ | |
| B5 | Add #378 Industrial Throughput (new endless, efficiency) | _pending_ | |
| B6 | Add Building slot endless node #384? (A=yes / B=defer / C=skip) | _pending_ | |

---

## 11. Source references

**Data files (verified 2026-07-09):**
- `sage-editor/SAGE Editor Suite/Research Nodes/research_nodes-careercombatspread.json` — 225 nodes total (26 Mining v1, 13 Building v1, 1 Mining v2, 6 Building v2)
- `sage-editor/CraftingTool/sage-c4-tools/public/data/claimStakeBuildings.json` — building data, scanned for tag references to verify dead-node claims
- `programs/sage/src/state/research.rs:165-179` — `ResearchNode` struct with `max_level` + `cost_growth_bps`

**Related docs:**
- [Endless Research Nodes — Program-Side Handoff](https://kingler959.github.io/kingler-audit-docs/endless-nodes-program-handoff.html) — Jacob's decision on diminishing-returns curve (Option A vs C)
- `sage-editor/SAGE Editor Suite/Research Nodes/MINING-BUILDING-TREE-REDESIGN-PROPOSAL.md` — original proposal (2026-07-08, contains the errors this doc corrects)

**Open PRs / branches:**
- Converter schema PR (pending) — adds `max_level` + `cost_growth_bps` emit to c4-converter
- `programs` repo `research/c4-rebalance` branch (Xcode, in progress) — XP curve flattening, tier-scaling, renown divisor changes

---

<div class="footer">
  <p><b>C4 Mining & Building Trees — Verified Structure + Proposed Changes</b> · 2026-07-09 · Kingler for Joseph Floyd</p>
  <p>All node IDs, names, CVCs, and tag references verified against SoT as of <code>sage-editor @ master (d21010b)</code>.</p>
</div>
