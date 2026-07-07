# C4 Cold-Start Audit & Decision Doc

**Star Atlas · C4 Progression**
**Date:** 2026-07-07
**Author:** Kingler (AI) for Joseph Floyd
**Status:** Draft — pending team review
**Audience:** bravetarget, bunthius, Arades

---

## How to record your decision

1. Open the rendered doc: https://kingler959.github.io/kingler-audit-docs/
2. Scroll to **Section 8 — Decision Record**.
3. Pick a verdict from each dropdown, add your rationale in the text box.
4. Click **Export** → choose Markdown or JSON.
5. Send the file back to Joseph.

Your responses stay in your browser until you export — nothing is sent anywhere, no login required.

---

## 1. Executive Summary

This audit answers two questions raised after the bunthius conversation on PR #173:

1. **Can a fresh character perform at least one action in each of the 6 careers immediately after creation?**
2. **How long does it take to unlock the first career branch node through natural play?**

**Short answer:** Yes — the current starter bundle (with the two agreed additions: Cultivation Claims + Beginner Stimulants) supports at least one action in all 6 careers. And the cold-start is **much faster than originally estimated** — 18 career levels (the threshold for unlocking the first Freelance node via the renown funnel) is achievable in **~14 minutes of active play**.

**Three caveats** surfaced during verification that need design attention before launch:

- **Scan XP formula may be too generous** — a single scan awards **~520 DataRunner XP** (enough for L6 in one action). Either intended, or `scan_power` should not multiply XP.
- **Combat cold-start has no survivable path** — the spawn ship (Fimbul Airbike, 35 HP) dies in 1 hit to any real target. Stims don't fix this.
- **Building XP is opaque** — the `xp_value` field isn't on claim stakes or in any checked artifact; it's uploaded server-side at deploy time.

---

## 2. Per-Career Bootstrap Matrix

Spawn ship: **Fimbul Airbike** (Default Config 101, XxSmall). All numbers verified against `programs/sage/src/`.

| Career | Cheapest First Action | Time / Action | XP / Action | Bundle Covers? |
|---|---|---|---|---|
| **Pilot** | Subwarp 0.1 AU | ~12 sec | 1 XP | ✅ Yes — 250k Fuel = 48k subwarps |
| **Data Runner** | Broad Spectrum scan (pattern #0) | **786 sec (13.1 min)** | **~520 XP** ⚠️ | ✅ Yes — 10k SDUs = 454 scans |
| **Mining** | Mine asteroid ore + `stop_mining` | ~1 sec to stop | `xp_modifier × amount` | ✅ Yes — 250k Ammo + 100k Food |
| **Building** | Place Claim Stake T1 + finalize | instant | `building_def.xp_value × qty` | ⚠️ Partial — 10 T1 stakes, ceiling unknown |
| **Crafting** | Craft Ammunition (recipe #0) | 1 sec | **20 XP** | ✅ Yes — 25k Copper + 1k ATLAS |
| **Combat** | Attack starbase (1 HP damage) | 1 round (~30 sec) | **8000 XP** (1 HP × CSS xp_value) | ❌ Gap — Fimbul dies in 1 hit |

**Bunthius confirmation (2026-07-07):** "it just happens automatically — no need to pick. If you move a ship you automatically get pilot xp." Verified in source — every career's gameplay instruction calls `collect_xp` on the correct `XpCategory`. No explicit career selection step exists or is needed.

---

## 3. Verified XP Formulas (from programs source)

Every formula below was located in the actual Solana program source and read in context. Line numbers are stable as of `main @ 7930598`.

| Career | Source (file:line) | Formula | Worked Example (Fimbul Airbike) |
|---|---|---|---|
| **Pilot** | `state/hangar/fleet/state.rs:1283` | `subwarp_xp_rate × progress` | 1 XP per completed subwarp |
| **Data Runner** | `instructions/scanning/scan.rs:302-309` | `base_xp × scan_power` | ⚠️ 1 × 520 = 520 XP per scan (L6 threshold = 500) |
| **Mining** | `instructions/mining/stop_mining_asteroid.rs:187` | `resource.xp_modifier × amount` | 1.0 × mined units (most ores) |
| **Crafting** | `instructions/crafting/complete_crafting_process.rs:145-150` | `recipe.value × quantity` | Ammunition: 20 × 1 = 20 XP/craft |
| **Combat** | `state/hangar/fleet/combat.rs:945-948` | `hp_damage_dealt × victim.xp_value` | 1 HP on CSS starbase (xp_value=8000) = 8000 XP |
| **Building** | `instructions/claim_stakes/finalize_building_changes.rs:143-146` | `building_def.xp_value × change_amount` | Unknown — `xp_value` not in checked artifacts |

### Scan cooldown units — verified

The `scan_cool_down: 786` value is in **seconds**, not milliseconds or U16F16 fractional. Confirmed at `scan.rs:300`:

```rust
// current_time is unix timestamp in seconds (i64)
let current_time = ctx.get_clock()?.unix_timestamp;
// ...
fleet_data.scan_cooldown_expires_at =
    current_time + (scan_cool_down * scan_pattern.cooldown_multiplier.0).to_num::<i64>();
```

So **13.1 minutes per scan is real**. The scan cooldown field is declared `U16F16` at `stats.rs:702`, but with raw value 786 it resolves to 786 whole seconds.

---

## 4. Wall-Clock Time to Milestones

Level thresholds (verified in `level_thresholds`): **L1=1, L2=100, L3=200, L4=300, L5=400, L6=500** (absolute XP, same for all 6 career tracks).

### Per career, fastest realistic time to hit L6 (500 XP):

| Career | Actions to L6 | Wall-clock | Notes |
|---|---|---|---|
| **Data Runner** | 1 scan | ~13 min | 520 XP > 500 threshold ⚡ |
| **Combat** | 1 attack | ~30 sec | 8000 XP from 1 HP on starbase ⚡ |
| **Crafting** | 25 crafts | ~25 sec | 20 XP/craft (Ammunition recipe) ⚡ |
| **Mining** | ~500 units | ~30 min | 0.262 units/sec mining rate |
| **Pilot** | 500 subwarps | ~100 min | Slowest "pure" grind |
| **Building** | unknown | unknown | `building_def.xp_value` not in artifacts |

### The 18-level cold-start (unlock first Freelance node)

To buy the first career's Freelance node, the player needs **3 CouncilRank XP**. Via the renown funnel (`DEFAULT_RENOWN_DIVISOR = 6`), that's **18 total career levels** across any combination of careers.

**Fastest viable cold-start path:**
1. **1 scan** → L6 Data Runner (520 XP, 13 min) — **6 levels**
2. **25 Ammunition crafts** → L6 Crafting (500 XP, 25 sec) — **6 levels**
3. **1 starbase shot** → L6+ Combat (8000 XP, 30 sec) — **6+ levels**

**Total: 18 career levels in ~14 minutes of active play.** Reasonable cold-start — **not the 16-day grind originally communicated in PR #173**, which was based on an incorrect 1-XP-per-scan assumption.

> **Important correction to PR #173 framing:** The "3 buys + 1 action" estimate was wrong. The accurate count is "3 CouncilRank XP worth of career levels" = 18 levels total, which the XP rates above make achievable in minutes rather than days. **PR #173's data fix (node renames) and simulator presets remain correct and shippable as-is.**

---

## 5. Starter Bundle Assessment

Source: `zink-web/packages/zink-profile-api/src/constants/faucet.constants.ts` → `C4_STARTER_BUNDLE_TOKENS`

| Category | Items | Verdict |
|---|---|---|
| **Resources** | 250k Ammo, 100k Food, 250k Fuel, 10k Repair Kit, 25k Diamond, 25k Hydrogen | ✅ Good |
| **Crafting Mats** | 21 types × 25k each (Copper, Iron, Steel, Titanium, Copper Wire, Polymer, Electronics, Framework, Graphene, ...) | ✅ Good — enough for ~1,000 Ammunition crafts |
| **Survey Data Units** | 10,000 SDUs (cargo id 366) | ✅ Good — 454 scans worth, covers L5+ Data Runner |
| **Claim Stakes** | T1×10, T2×10, T3×5, T4×5, T5×5 | ⚠️ Limited — 35 total placements, Building ceiling depends on `xp_value` |
| **Crafting Habs** | T1-T5 × 5 each | ⚠️ Limited — same Building ceiling concern |
| **Ships** | Fimbul Airbike ×34, Pearce X5 ×21, Busan ×13, Mamba ×8, Bitboat ×5, Guardian ×3 | ℹ️ Pre-stocked — only the 34 XxSmall Fimbuls are flyable at spawn |
| **Currency** | 10 SOL, 1000 ATLAS | ✅ Good — ATLAS covers ~1,000 crafting fees |
| **+ Cultivation Claims** *(agreed)* | Pending mint/quantity from bravetarget | ✅ Needed — closes cultivation branch of Building |
| **+ Beginner Stimulants** *(agreed)* | Pending mint/quantity from bravetarget | ✅ Useful — buff versatility (does not fix Combat survivability) |

---

## 6. Key Findings & Corrections

### Corrections to earlier analysis

| Earlier Claim | Actual | Impact |
|---|---|---|
| Scans award 1 XP each | **Scans award ~520 XP each** (1 × scan_power) | ✅ Cold-start is 500× faster than estimated |
| Ammunition recipe gated by tag 136 (Complex Crafting) | **Ammunition has `research_requirements: []`** — zero gate | ✅ Fresh character can craft basic consumables immediately |
| Cold-start requires ~1,200 gameplay actions | **~27 actions** (1 scan + 25 crafts + 1 attack) for 18 levels | ✅ Reasonable onboarding curve |
| SDUs missing from starter bundle | **10,000 SDUs present** (cargo id 366) | ✅ Data Runner fully bootstrappable |

### Remaining concerns

1. **Scan cooldown UX.** 13 minutes for the first scan is a poor first-impression, even though the XP reward compensates. Consider lowering cooldown AND the XP reward proportionally — same total XP/hour, better pacing.
2. **Combat cold-start is a suicide run.** Fimbul Airbike (35 HP) vs CSS starbase (30k dmg/round) = 1-shot death. The player gets 8000 Combat XP but loses the ship. Either add a basic weapon module, spawn a training NPC, or accept this as intended.
3. **Building XP is opaque.** `building_def.xp_value` is set server-side at deploy time and isn't in any universe.json artifact. Can't compute time-to-L2 Building without it.
4. **Bigger ships unusable at spawn.** Pearce X5 (XSmall) through Guardian (Capital) are pre-stocked but unusable until Pilot tree progression unlocks larger `max_ship_size`. Intended behavior, but worth calling out — players may be confused why they "have" ships they can't fly.

---

## 7. Open Decisions *(needs sign-off)*

Each decision is scoped to be answerable with one of: **Accept / Change / Defer**.

### D1 · Scan XP formula `[design]`
- **Owner:** bunthius / design
- **Impact:** Data Runner balance
- **Urgency:** pre-launch
- **Question:** Is `final_xp = base_xp × scan_power` (`scan.rs:302-303`) the intended formula? With Fimbul Airbike's `scan_power=520` and `blank_xp_value=1`, this means **one scan = L6 Data Runner**.
- **If intended:** Accept. Data Runner becomes the fastest career to bootstrap, balanced by the 13-min cooldown.
- **If not intended:** Likely the formula should be `base_xp` only (1 XP/scan), with `scan_power` multiplying loot amount only. In that case, add a separate game balance ticket — the cold-start numbers in this doc would shift by ~500×.

### D2 · Combat cold-start survivability `[gap]`
- **Owner:** design + bravetarget
- **Impact:** Combat career onboarding
- **Urgency:** pre-launch
- **Question:** How should a fresh player earn their first Combat XP without losing their only ship?
- **Options:**
  - **A.** Add a basic weapon module to the starter bundle.
  - **B.** Spawn a "training NPC" at the CSS starting system.
  - **C.** Accept the suicide-run pattern (player replaces Fimbul from bundle stock of 34).
  - **D.** Defer to post-launch — Combat is optional for cold-start.

### D3 · Building XP ceiling `[data gap]`
- **Owner:** bunthius / server deploy
- **Impact:** Building career onboarding
- **Urgency:** pre-launch
- **Question:** What is `building_def.xp_value` for Claim Stake T1-T5 and Crafting Hab T1-T5? This is set via `UpdateBuildingDefinition` at game deploy and isn't in any checked artifact.
- **Why it matters:** The bundle has 35 Claim Stakes + 25 Crafting Habs = 60 placements. If each placement is worth 1 XP, Building caps at L1. If worth 10 XP, caps at L2. Need actual numbers to compute time-to-L6 Building.
- **Resolution path:** Share the C4 init config or query the deployed game state.

### D4 · Scan cooldown pacing `[ux]`
- **Owner:** design
- **Impact:** First-scan player experience
- **Urgency:** pre-launch (if D1 = accept)
- **Question:** If D1 is accepted (scan = 520 XP), should the 786-second cooldown be lowered for better pacing? Same XP/hour either way, but a 13-minute wait for the first scan is a poor first impression.
- **Suggestion:** Lower to ~60-90 sec cooldown, scale XP proportionally (~40-65 XP/scan). Player still hits L6 in 8-13 scans but gets feedback faster.

### D5 · Bundle additions — confirm specifics `[action]`
- **Owner:** bravetarget
- **Impact:** Starter bundle contents
- **Urgency:** pre-launch
- **Already agreed:**
  - Cultivation Claims (closes Building cultivation branch)
  - Beginner Stimulants (buff versatility)
- **Needed from bravetarget:** mint addresses, cargo IDs, and quantities for both. Once provided, can draft the TypeScript addition to `C4_STARTER_BUNDLE_TOKENS` directly.

### D6 · Ship-size communication `[minor]`
- **Owner:** fc-ui
- **Impact:** Player confusion
- **Urgency:** post-launch OK
- **Question:** The bundle includes 5 ship sizes (XSmall → Capital) but only XxSmall is flyable at spawn. Should the UI indicate this clearly, or leave as "discovered through play"?
- **Note:** Out of scope for this audit, but flagged here so it doesn't get lost. Belongs in a future fc-ui polish ticket.

---

## 8. Decision Record

> **Workflow:** Fill in the interactive form on the [rendered HTML page](https://kingler959.github.io/kingler-audit-docs/#decision-record) — pick a verdict from each dropdown, add your rationale, then click **Export** to download a Markdown or JSON file. Send the file back to Joseph.
>
> Verdict values: **Accept** · **Change** · **Defer** · **Needs discussion**

| # | Decision | Owner | Verdict | Rationale | Date |
|---|---|---|---|---|---|
| D1 | Scan XP formula (`base × scan_power`) — intended? | bunthius / design | _pending_ | | |
| D2 | Combat cold-start survivability (weapon module? training NPC? suicide-run? defer?) | design + bravetarget | _pending_ | | |
| D3 | Building XP ceiling — what is `building_def.xp_value`? | bunthius / deploy | _pending_ | | |
| D4 | Scan cooldown pacing (786s → 60-90s?) | design | _pending_ | | |
| D5 | Bundle additions — confirm Cult Claims + Stims mints/IDs | bravetarget | _pending_ | | |
| D6 | Ship-size communication in UI | fc-ui | _pending_ | | |

### Change log

- _2026-07-07 — Decision Record created (Kingler). All 6 decisions marked `pending`._

---

## 9. Data Gaps

| Gap | Why It Matters | Where to Find It |
|---|---|---|
| `building_def.xp_value` for Claim Stakes & Crafting Habs | Can't compute time-to-L6 Building | C4 init config / `UpdateBuildingDefinition` admin uploads / deployed on-chain game state |
| Survey Data Unit cargo ID confirmation | Pattern cost references token id 3 (which maps to Repair Kit, not SDU). Scan cost semantics may differ from raw cargo cost. | `scan.rs` full context or design confirmation |
| Cultivation Claim & Beginner Stimulant mints/IDs | Can't draft the bundle PR addition without them | bravetarget |
| Resource `xp_modifier` values across all 56 ore/deposit types | Mining XP per resource varies; only sampled common ores (=1.0) | `cargo_types` in universe.json — full pass needed |
| Runtime faucet distribution logic | Constants are read; whether the faucet actually mints all listed tokens at claim time is server-side | `zink-web` server code (not in client repo) |

---

## 10. Source References

### Primary program sources (verified line numbers)

- `programs/sage/src/instructions/scanning/scan.rs:119,300,302-309` — scan cooldown + XP formula
- `programs/sage/src/state/hangar/stats.rs:702` — `scan_cool_down: U16F16` declaration
- `programs/sage/src/instructions/crafting/complete_crafting_process.rs:145-150` — Crafting XP
- `programs/sage/src/state/hangar/fleet/combat.rs:939-948` — Combat XP formula
- `programs/sage/src/instructions/claim_stakes/finalize_building_changes.rs:143-146` — Building XP
- `programs/sage/src/state/hangar/fleet/state.rs:1279-1283` — Pilot XP on subwarp completion
- `programs/sage/src/instructions/mining/stop_mining_asteroid.rs:187` — Mining crew XP pour
- `programs/sage/src/state/claim_stakes.rs:131` — `BuildingDefinition.xp_value` declaration

### Data artifacts

- `sage-editor/_out/universe.json` — 1238 recipes, 61 ships, 157 research nodes, 5 scan patterns, 945 systems
- `programs/cli/c4-cli/conf/{deploy,test,zink-testnet}.json` — all 3 confirmed missing `building_definitions`
- `zink-web/packages/zink-profile-api/src/constants/faucet.constants.ts` — `C4_STARTER_BUNDLE_TOKENS`

### Ship stats (Fimbul Airbike Default Config 101)

```
scan_cool_down: 786          # seconds (13.1 min)
scan_power: 520              # multiplies base_xp AND loot amount
scan_cost: 22                # Survey Data Units per scan
subwarp_speed: 0.0084        # AU/sec
subwarp_fuel_consumption: 5.15
warp_fuel_consumption: 18.76
asteroid_mining_rate: 0.262  # units/sec
asteroid_mining_ammo_rate: 0.018
asteroid_mining_food_rate: 0.014
cargo_capacity: 249
fuel_capacity: 450
ammo_capacity: 104
hit_points: 35               # dies in 1 hit to any real target
shield_points: 24
subwarp_xp_rate: 1
warp_xp_rate: 1
```

### Related PRs

- **sage-editor PR #173** — [3 node renames + 6 cold-start simulator presets](https://github.com/staratlasmeta/sage-editor/pull/173) (data fix — shippable as-is)
- **star-atlas-tech PR #4967** — [client UI fixes: gateway nodes visible, gameplay-XP hints, Career Unlocks label](https://github.com/staratlasmeta/star-atlas-tech/pull/4967)

---

*C4 Cold-Start Audit & Decision Doc · 2026-07-07 · Kingler for Joseph Floyd*
*Numbers verified against `star-atlas-tech @ main (7930598)` and `sage-editor @ claude/c4-progression-tree-view`.*
