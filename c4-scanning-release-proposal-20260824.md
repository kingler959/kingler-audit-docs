# C4 Scanning — Release Gameplay Proposal

**Date:** 2026-08-24

**Status:** Draft for product, economy, Programs, SES, and FC App sign-off

**Rendered URL:** https://kingler959.github.io/kingler-audit-docs/c4-scanning-release-proposal-20260824.html

**Current-state baseline:** Programs `d4fd6898`, SAGE Editor `2d0e1863`, FC App `665a973c`

## Recommendation

Ship scanning as an **exploration-and-recovery career**, not an SDU faucet and not a menu slot machine.

The recommended release loop is:

1. **Read the map:** choose a Region and interpret visible signal conditions.
2. **Fit the fleet:** choose a pattern, Scanner Charge supply, cargo room, and scanner-focused hull/config.
3. **Detect:** scan to commit cost and create one bounded signal for that fleet.
4. **Move:** travel to the recovered coordinate before the signal expires.
5. **Recover:** reveal the committed outcome and collect direct loot.
6. **Analyze and specialize:** use or sell materials and Data Cubes; progress pattern, Region, quality, and cadence branches.
7. **Move on:** exhausted signals and one-active-signal rules make exploration more valuable than parking.

### Release reward posture

- **Primary:** direct, useful cargo—materials, consumables, components, and rare research commodities.
- **Rare career artifacts:** Rare, Epic, Legendary, and Anomalous Data Cubes.
- **Not at release:** generic randomized loot boxes. No authoritative source currently commits scanning to loot boxes, while the research/data model explicitly calls for real Data Cube cargo and scan mappings.[6][13]
- **Post-release option:** an earned-only Encrypted Cache can be evaluated after real telemetry, but its contents must be committed at scan time, odds disclosed, and no paid key or reroll sold.

## Why this should be the release target

Current scanning is a single transaction, a cooldown, and a weighted cargo roll. The caller selects a pattern; Programs evaluates coordinate/time noise, chooses blank or one eligible static row, scales quantity linearly by scan power, clips it to cargo capacity, and awards flat XP.[1][2]

The five emitted patterns currently differ primarily by procedural noise field and nominal SDU amount.[3][4]

That is enough machinery for a proof of concept, but not enough player agency for a career. The player cannot read the live signal, understand actual odds, choose a semantic destination, or do anything after pressing Scan beyond waiting for cooldown.[8][9]

The dormant advanced dataset proves that loot-oriented categories have already been explored—common supplies, ores, refined materials, weapons, electronics, rare materials, titan components, and stimulants—but its 85 rows are shadowed by colliding IDs and are not release-ready.[5]

## Current state versus proposed release

| Area | Current | Recommended release |
|---|---|---|
| Core action | Select pattern → immediate roll | Detect → travel → recover |
| Location | Raw X/Y/time procedural noise | Authoritative Region profile + local signal target |
| Rewards | One SDU row per pattern | Direct materials/components + Data Cubes |
| Pattern choice | Mostly linear payout tiers | Five horizontal strategies with distinct reasons to choose |
| Failure | Blank result after full cost | No-contact result: lower XP, readable feedback, no full reward |
| Scanner ships | Fast/powerful but currently zero scan cost | Fast, precise, cheaper—not free—and better at interpretation |
| Quantity | Linear `output × scan_power`; widespread cargo clipping | Fixed discrete drops; square-root bulk scaling with a hard cap |
| Progression | Pattern/cube/Region branches exist but content wiring is incomplete | Staggered pattern unlocks, cube rarities, Region access, quality and cadence |
| Randomness | Latest slot hash at immediate scan | Future-hash commit/reveal; outcome fixed before player can know it |
| Loot boxes | No current authoritative implementation or config | Explicitly deferred |

## Proposed gameplay loop

### 1. Read the map

The galaxy map shows **signal climate**, not a shopping list:

- current Region risk and faction context;
- dominant signal categories: industrial, technological, tactical, exotic;
- signal strength band: weak, stable, strong, volatile;
- recent local exhaustion;
- patterns the selected fleet can run.

The exact item remains unknown. The player receives enough information to make a route decision without turning exploration into deterministic vending.

### 2. Fit the fleet

Preflight shows:

- Scanner Charges required;
- scan cooldown and expected total loop time;
- cargo room after charges are consumed;
- signal-quality contribution;
- bulk-yield multiplier;
- research/Region locks by player-facing node name;
- whether another unresolved signal blocks this fleet.

### 3. Detect

A scan:

- consumes charges;
- resolves the fleet's Region authoritatively;
- selects the Region loot profile and chosen pattern;
- commits a future entropy slot and reward envelope;
- creates at most one `ScanSignal` per fleet;
- returns either **No Contact** or a target signature.

A target signature includes category, rarity band, target coordinate/radius, expiration, and risk—not the exact reward.

### 4. Move and recover

The fleet travels to the target and runs Recover before expiry. Recovery:

- verifies the same fleet is inside the radius;
- reveals the future-hash-committed outcome;
- deposits direct cargo using fixed or bounded scaling;
- awards the full Data Runner XP;
- clears the active signal.

Travel is the missing verb in the current loop. It creates route choice, exposure, fuel cost, ship identity, and opportunities for future encounters.

### 5. Analyze, trade, and specialize

Rewards feed other systems:

- common materials support operation and crafting;
- components improve fleets or enter the market;
- Data Cubes unlock research and become tradeable career commodities;
- high-risk signals can later branch into NPC markets, missions, or faction discoveries.

## Pattern identities

Patterns should be **horizontal strategies**, not five versions of “bigger number.”

| Pattern | Unlock | Player purpose | Contact chance* | General loop* | Specialist loop* | Reward identity |
|---|---:|---|---:|---:|---:|---|
| **Broad Spectrum** | Starter | Reliable survey and route discovery | 85% | 15 min | 6 min | Common supplies, raw materials, broad Region sampling |
| **Focused Array** | Data Runner 8 | Choose Industrial / Tech / Tactical focus | 80% | 17 min | 7 min | Lower breadth, better category control |
| **Enhanced Signal** | Data Runner 15 | Quality-focused specialist sweep | 72% | 20 min | 8 min | Refined materials, electronics, specialist components |
| **Deep Resonance** | Data Runner 25 + Deep Space | High-risk rare-material hunting | 65% | 24 min | 10 min | Rare ores, advanced components, Data Cubes |
| **Spatial Anomaly** | Data Runner 38 + Anomalous Cube | Event and discovery hunting | 50% | 32 min | 14 min | Exotic artifacts, Anomalous Cubes, future encounter hooks |

\*Proposal tuning assumptions, not current runtime facts.

### Suggested rarity mix within successful recoveries

| Pattern | Common | Uncommon | Rare | Epic | Legendary | Anomalous |
|---|---:|---:|---:|---:|---:|---:|
| Broad | 72% | 23% | 5% | — | — | — |
| Focused | 48% | 36% | 14% | 2% | — | — |
| Enhanced | 25% | 40% | 27% | 7% | 1% | — |
| Deep | 8% | 27% | 42% | 18% | 5% | — |
| Spatial | — | 12% | 43% | 29% | 13% | 3% |

Research gates add higher tiers to the eligible pool. Locked high-tier weight must be redistributed among eligible lower tiers, not converted into extra blank probability.

## Reward architecture

### Direct loot is the foundation

Use the dormant advanced table as a **catalog seed**, not as a deployable table.[5]

- Broad: Food, Fuel, Repair Kits, common ore and common refined materials.
- Focused: player-selected Industrial, Technology, or Tactical families.
- Enhanced: electronics, control circuits, sensor elements, energy cells, specialist components.
- Deep: rare ores, refined rare materials, advanced components, Data Cubes.
- Spatial: exotic cores, titan-grade components, rare stimulants, Anomalous Data Cubes, encounter hooks.

Do not let scanning bypass the entire crafting economy. Drop a mixture of raw materials, partial components, and occasional finished items; use economy-owned allowlists and per-Region value budgets.

### Data Cubes are not loot boxes at release

The existing progression already defines Data Cube Analysis and Rare/Epic/Legendary/Anomalous refinement nodes.[6] A prior decision record explicitly chose real Data Cube cargo rows and scanning mappings rather than inert labels.[13]

For release:

- author four Data Cube cargo types;
- make them tradable research/crafting commodities;
- use previous-tier cubes and normal tech components for later research costs;
- do **not** require a cube to unlock its own first acquisition;
- do **not** make cubes randomized containers yet.

Suggested progression costs after SDU retirement:

| Node | Replace SDU cost with |
|---|---|
| Data Cube Analysis | Electronics + Control Circuits |
| Rare Cube Refinement | Sensor Elements + Signal Amplifier Array |
| Epic Cube Refinement | Rare Cubes + Control Circuits |
| Legendary Cube Refinement | Epic Cubes + Quantum Processor |
| Anomalous Cube Refinement | Legendary Cube + Exotic Matter Stabilizer |
| Signal Amplification / Rapid Cycling | scanner components appropriate to tier |

This closes the scan → research → better scan loop without inventing SDU under another name.

### Quantity scaling must change

Current loot quantity is linear in scan power and then clipped by cargo capacity.[1] That is unsuitable for discrete components or one-of-one artifacts; even the current Airbike can generate nominal tens of thousands of SDU from the smallest row before clipping.[3]

Recommended output modes:

```text
Fixed
  components, Data Cubes, stimulants, artifacts
  quantity is the authored integer; scan power does not multiply it

BulkSqrt
  raw/refined materials and common consumables
  multiplier = clamp(0.75, 2.25, sqrt(effective_scan_power / 500))
```

Examples:

- Airbike power 520 → about `1.02×` bulk yield.
- Opal Rayfam Scanning Max power 1,330 → about `1.63×`.
- Fimbul BYOS Ranger Scanning Max power 1,470 → about `1.71×`.
- VZUS opod Scanning Max power 1,540 → about `1.75×`.
- research/crew stacking cannot exceed `2.25×` bulk yield.

FC must show both nominal and cargo-capped quantity before commitment.

## Specialist Data Runner ships

Three current hulls are explicitly authored with `Spec: Data Runner`:

| Hull | Size | Base power | Base cooldown | Cargo | Current scan cost |
|---|---|---:|---:|---:|---:|
| Opal Rayfam | Small | 950 | 312 s | 5,640 | 0 |
| Fimbul BYOS Ranger | Medium | 1,050 | 300 s | 16,652 | 0 |
| VZUS opod | Medium | 1,100 | 300 s | 13,781 | 0 |

The hull metadata and scanning loadouts confirm the intended specialist role.[10][11][12]

### Recommended specialist contract

Data Runner hulls should win through **information and cadence**, not an uncapped loot multiplier:

- preserve their materially shorter cooldowns and stronger Scanner Array/Scan Drone loadouts;
- `+10` normalized signal-quality score;
- `+50%` signal expiration window;
- `-25%` Scanner Charge use, rounded up with a hard minimum of one;
- one additional preview detail—category, risk modifier, or tighter target radius;
- no zero-cost scanning;
- no exclusive access to the career itself.

General ships can scan. Data Runner ships make scanning a profession.

## World-derived loot

Ordinary scanning currently evaluates procedural noise at raw coordinates and time; it does not inspect nearby planets, systems, asteroids, or Region resources.[2]

The final design should add bounded **Region loot profiles**:

1. SES authors one stable profile ID per Region.
2. The converter compiles system/planet resource membership, Region risk, faction context, and approved content families into that profile.
3. Programs requires an authoritative RegionTracker and resolves the fleet coordinate itself.
4. The selected pattern filters/modifies the Region profile.
5. The client cannot substitute a more valuable profile account.

Risk multiplies the profile's value budget:

- Low risk: `1.0×`
- Medium risk: `1.5×`
- High risk: `2.25×`

The multiplier raises expected value and eligible rarity, not every item quantity blindly.

## Progression

The current SoT already contains most of the correct career skeleton: Region access, cube analysis, pattern refinement, Sensor Mastery, Signal Amplification, Rapid Cycling, and a level-40 Master Data Runner capstone.[6]

### Recommended level journey

| Level | Milestone | Gameplay change |
|---:|---|---|
| 0 | Broad Spectrum | Basic Region survey and common loot |
| 2 | Freelance Data Runner | Career begins |
| 3 | Data Cube Analysis + Regional Tiers | Cubes become meaningful; Region branch opens |
| 5 | Contested Space Scanning | Medium-risk profiles |
| 8 | Rare Cube + Sensor Mastery + Focused Array | First specialization decision |
| 10 | Signal Amplification I | Better bulk yield |
| 12 | Rapid Cycling I | Better cadence |
| 15 | Epic Cube + Enhanced Signal | Advanced tech/component hunting |
| 18 | Deep Space Scanning | High-risk profiles |
| 20 | Signal Amplification II | Stronger yield |
| 22 | Enemy Faction Scanning | Enemy-faction profile access |
| 24 | Rapid Cycling II | Higher cadence |
| 25 | Legendary Cube + Deep Resonance | Rare-material profession |
| 30 | Deep Signal Refinement + Amplification III | Master-quality sensing |
| 36 | Rapid Cycling III | Maximum cadence |
| 38 | Anomalous Cube + Spatial Anomaly | Exotic discoveries |
| 40 | Master Data Runner | Full cross-branch capstone |

Do not unlock all five patterns together behind Signal Refinement as the current raw tree effectively does. Stagger them so each career phase changes the player's decisions.

### Release-bridge pacing

Recommended bridge XP until the separately gated XP-v1 migration activates:

- No Contact: `10` Data Runner XP.
- Successful recovery: `52` Data Runner XP total.
- Abandoned or expired signal: no recovery XP.
- Most XP settles at recovery, not scan initiation.

Using the current legacy Data Runner thresholds and the proposal's Broad loop assumptions:

| Level | Cumulative XP | General scanner | Specialist scanner |
|---:|---:|---:|---:|
| 8 | 804 | ~4.4 h | ~1.8 h |
| 15 | 2,180 | ~11.9 h | ~4.8 h |
| 25 | 6,010 | ~32.9 h | ~13.2 h |
| 38 | 18,277 | ~100 h | ~40 h |
| 40 | 21,506 | ~117.6 h | ~47.1 h |

These are design-model hours, not promises; travel distance, Region risk, failed recoveries, competition, and actual session behavior will move them.

### XP-v1 dependency

A separate, currently disabled XP-v1 source proposes `1 XP` for an unsuccessful scan and `10 XP` for success, multiplied by raw acting-fleet ship count, with a 3,947 XP/day Data Runner budget.[7]

That rollout must remain a separate decision gate. Raw ship-count scaling can make a many-small-ship fleet a better career trainer than one specialist hull, which conflicts with the Data Runner fantasy. Before activation, compare raw ship count against a bounded `scanner_units` measure derived from effective scan power plus the Data Runner role.

## Pacing and relative value model

`Value Unit (VU)` is a relative economy budget for comparison, not ATLAS and not a promised item price.

| Pattern | Expected VU / loop | General VU / h | Specialist VU / h | General XP / h | Specialist XP / h |
|---|---:|---:|---:|---:|---:|
| Broad | 8.8 | 35.2 | 88.0 | 182.8 | 457.0 |
| Focused | 11.6 | 40.9 | 99.4 | 153.9 | 373.7 |
| Enhanced | 16.68 | 50.0 | 125.1 | 120.7 | 301.8 |
| Deep | 26.1 | 65.2 | 156.6 | 93.2 | 223.8 |
| Spatial | 42.5 | 79.7 | 182.1 | 58.1 | 132.9 |

Higher patterns pay more value but less XP per hour. Career progression does not force players to farm the most economically valuable pattern, and economic hunting does not automatically maximize career speed.

## Anti-farm and integrity rules

1. **One active signal per fleet.** No scan carousel while ignoring recoveries.
2. **Future-hash reveal.** The deciding entropy must not exist when cost is committed.
3. **Outcome fixed at commit.** Abandoning cannot reroll into a better item.
4. **Recovery required.** Full reward and most XP settle only at the target.
5. **No-contact costs remain sunk.** Failure is legible, not free.
6. **Regional signal exhaustion.** Repeated recoveries in one Region reduce rare-profile availability; movement restores opportunity.
7. **Bounded quantity modes.** Fixed discrete drops and capped square-root bulk scaling.
8. **Nonzero charge floor.** Dedicated hulls are efficient, never free.
9. **Capacity-aware preflight.** The UI warns when valuable output would be clipped.
10. **Server/program authority.** Region, profile, signal, target, and reward envelope are not client-selected.
11. **Telemetry:** attempts, contacts, recoveries, expirations, abandons, reward VU, clipping, Region/pattern/hull, and time-to-recover.

## FC App experience

### Map

- signal climate overlay by Region;
- visible risk/value band;
- local exhaustion indication;
- unresolved signal marker with TTL;
- selected fleet's reachable patterns.

### Pattern chooser

Each unique pattern gets one consolidated row:

- purpose and unlock;
- exact charge cost;
- actual cooldown;
- contact estimate and rarity ceiling;
- Region category mix;
- fleet quality/yield/TTL effects;
- cargo clipping warning;
- named research locks.

### Findings panel

Show:

- Contact / No Contact;
- signature category and rarity band;
- target distance, radius, and expiration;
- committed cost;
- Recover CTA;
- on recovery: exact item rows, quantities, XP, Region/pattern/hull context.

The client should stop presenting static noise-weight sums as if they were current signal and should remove stale XP-per-power copy.[8][9]

## Technical contract

### New accounts/config

- `ScanSignal` PDA: Game + Character + Fleet; one active state, pattern, Region/profile, commitment slot/hash target, target coordinate/radius, expiration, reward commitment/version.
- `ScanLootProfile`: bounded Region-owned tables and value budget.
- `ScanLootEntry` extension: `quantity_mode = Fixed | BulkSqrt`, rarity, category, optional research gates.
- Region profile reference in SES/converter output.

Use new accounts rather than widening Character.

### Instructions

- `DetectSignal`: validates idle fleet, Region, pattern, research, charge/cooldown, and absence of an active signal; commits future entropy.
- `RecoverSignal`: validates owner/fleet/location/TTL, reveals committed outcome, emits cargo, awards recovery XP, clears signal.
- `AbandonSignal`: clears state without reroll reward; applies a short lockout or preserves the original cooldown.
- `ExpireSignal`: permissionless or owner-triggered cleanup after TTL.

### Existing systems to reuse

- pattern accounts and noise maps;
- RegionTracker coordinate resolution;
- future-slot-hash commit/reveal approach already present in encounter work;
- research tags and Data Runner modifiers;
- FC cargo-delta findings panel;
- SAGE Editor pattern authoring/converter pipeline.

## Release scope

### Required for sign-off-quality release

1. Direct-loot catalog and four Data Cube cargo rows.
2. Region loot profiles generated from current world data.
3. Fixed versus square-root quantity modes.
4. Detect/recover `ScanSignal` lifecycle with future-hash reveal.
5. Five differentiated, staggered patterns.
6. Data Runner hull cost normalization and role bonuses.
7. FC map/chooser/findings/recovery UX.
8. Research cost migration away from SDU.
9. Exact-head converter, Rust schema, program, FC, and chain-backed integration tests.
10. Telemetry and economy budget dashboards before mainnet tuning.

### Explicitly deferred

- randomized loot-box opening;
- paid keys or rerolls;
- player trading inside scan encounters;
- procedural mission chains;
- global/shared depletion requiring cross-player hot-state writes;
- combat scanner branch redesign;
- XP-v1 activation/migration unless its separate readiness record is complete.

### Estimated implementation

| Workstream | AI-assisted effort |
|---|---:|
| Product/economy tables + SES schema | 2–3 days |
| Programs accounts/instructions/randomness/scaling | 6–8 days |
| Converter/config/fixtures | 3–4 days |
| FC map, chooser, signal lifecycle, findings | 4–6 days |
| Integration, security, economy, and live-state validation | 4–5 days |
| **Total** | **19–26 AI-days**, plus human review and deployment coordination |

A compressed immediate-loot version can be smaller, but it should be described honestly as a launch fallback—not the recommended career loop.

## Rollout gates

1. Approve this product contract.
2. Freeze IDs and data ownership across Programs and SES.
3. Implement feature-flagged/new-account program path; preserve legacy scan until migration.
4. Generate current-target configs into isolated output; prove unrelated sections unchanged.
5. Run deterministic economic simulation across every hull/config, Region, pattern, rarity, and cargo-cap boundary.
6. Run commit/reveal adversarial tests: late reveal, replay, wrong fleet, wrong Region/profile, stale hash, abandon/reroll, full cargo, zero charges.
7. Deploy exact Programs/IDL/SDK/config pair to test cluster.
8. Run populated FC walkthrough with specialist and general hulls, screenshots, console, and transaction evidence.
9. Read back every pattern/profile and sample signal/reward account.
10. Tune via telemetry; no mainnet activation until economy and security sign off separately.

## Decision record

Use the rendered page to record Accept / Change / Defer / Needs discussion and export Markdown or JSON.

| # | Decision | Recommended owner |
|---|---|---|
| D1 | Make Detect → Move → Recover the release target | Product + Programs + FC |
| D2 | Replace SDU-primary rewards with direct loot + Data Cubes | Product + Economy |
| D3 | Defer generic randomized loot boxes until after release telemetry | Product + Economy |
| D4 | Use converter-generated Region loot profiles | SES + Programs + Economy |
| D5 | Adopt the five horizontal pattern identities and staggered levels | Product + Economy |
| D6 | Preserve Data Runner hull advantage but remove zero-cost scanning | Ships + Economy |
| D7 | Adopt Fixed/BulkSqrt scaling and the anti-reroll signal lifecycle | Programs + Economy |
| D8 | Use 10/52 bridge XP and keep XP-v1/raw-ship scaling as a separate gate | Progression + Programs |

## Known unknowns

- The user's report that loot boxes were discussed is credible team context, but no current authoritative gameplay repo or config commits scanning to loot boxes.
- Exact item value budgets require the economy owner's live market assumptions; VU is deliberately relative.
- Region profile derivation needs a separate exhaustive mapping review against current body-resource ownership.
- The current XP-v1 contract is disabled and has its own migration/readiness requirements.[7]
- The dormant advanced table is useful design evidence, not deployable balance.[5]

## Sources

[1] https://github.com/staratlasmeta/programs/blob/d4fd6898a7543232cc54b6b41f4da38e493ca5e6/programs/sage/src/instructions/scanning/scan.rs — Programs scan instruction
[2] https://github.com/staratlasmeta/programs/blob/d4fd6898a7543232cc54b6b41f4da38e493ca5e6/programs/sage/src/state/scan_pattern.rs — Programs ScanPattern state and noise evaluation
[3] https://github.com/staratlasmeta/programs/blob/d4fd6898a7543232cc54b6b41f4da38e493ca5e6/cli/c4-cli/conf/universe.json — Programs current universe configuration
[4] https://github.com/staratlasmeta/sage-editor/blob/2d0e18633565a0eb20d2f7078e02d61ae6f43acb/SAGE%20Editor%20Suite/C4%20Tools/data/scan_patterns_default.json — SAGE Editor default scan patterns
[5] https://github.com/staratlasmeta/sage-editor/blob/2d0e18633565a0eb20d2f7078e02d61ae6f43acb/SAGE%20Editor%20Suite/C4%20Tools/data/scan_patterns_advanced.json — SAGE Editor dormant advanced scan patterns
[6] https://github.com/staratlasmeta/sage-editor/blob/2d0e18633565a0eb20d2f7078e02d61ae6f43acb/SAGE%20Editor%20Suite/Research%20Nodes/research_nodes-careercombatspread.json — SAGE Editor Data Runner research tree
[7] https://github.com/staratlasmeta/sage-editor/blob/2d0e18633565a0eb20d2f7078e02d61ae6f43acb/SAGE%20Editor%20Suite/C4%20Tools/data/xp_config_v1.json — SAGE Editor proposed XP v1 runtime contract
[8] https://github.com/staratlasmeta/star-atlas-tech/blob/665a973c9ed358818783f3aa58869790814fdb6a/packages/fc-app/src/components/PixiMap/FleetInfoPanel.tsx — FC App scan pattern UI
[9] https://github.com/staratlasmeta/star-atlas-tech/blob/665a973c9ed358818783f3aa58869790814fdb6a/packages/fc-app/src/components/PixiMap/PixiMap.tsx — FC App scan submission flow
[10] https://github.com/staratlasmeta/sage-editor/blob/2d0e18633565a0eb20d2f7078e02d61ae6f43acb/SAGE%20Editor%20Suite/Ship%20Configurator/ships/3_Small_Opal_Rayfam_Opal.json — Opal Rayfam Data Runner hull
[11] https://github.com/staratlasmeta/sage-editor/blob/2d0e18633565a0eb20d2f7078e02d61ae6f43acb/SAGE%20Editor%20Suite/Ship%20Configurator/ships/4_Medium_Fimbul_BYOS_Ranger_Fimbul%20BYOS.json — Fimbul BYOS Ranger Data Runner hull
[12] https://github.com/staratlasmeta/sage-editor/blob/2d0e18633565a0eb20d2f7078e02d61ae6f43acb/SAGE%20Editor%20Suite/Ship%20Configurator/ships/4_Medium_VZUS_opod_VZUS.json — VZUS opod Data Runner hull
[13] https://github.com/jfloyd959/claude-brain/blob/ff8c6d3d7e7b1e61944b338c69e6902e00ba4508/c4-decisions-2026-06-15.md — C4 research-tree decision record

No live config, deployment, re-init, or chain write was performed.
