# C4 Scanning — Release Gameplay Proposal

**Date:** 2026-08-24

**Status:** Local draft revised for Michael Wagner's 2026-08-25 executive direction; not published

**Published URL (not updated by this local revision):** https://kingler959.github.io/kingler-audit-docs/c4-scanning-release-proposal-20260824.html

**Current-state baseline:** Programs `d4fd6898`, SAGE Editor `2d0e1863`, FC App `665a973c`

## Recommendation

Develop scanning toward an **exploration-and-recovery career**, not an SDU faucet and not a menu slot machine. This is the coordinated V2 direction, **not a Phase 3 blocker**: Phase 3 can ship the existing scanning implementation and its current Toolkit/Repair Kit scan cost unchanged while V2 work proceeds during and after Phase 3.

### Executive disposition — Michael Wagner, 2026-08-25

- **Direction approved; timing changed:** Detect → Travel → Recover is the V2 direction, but substantial design and implementation may happen during or after Phase 3. It is not a hard Phase 3 rollout requirement.
- **Phase 3 bridge approved:** current scanning can ship in Phase 3 unchanged, including its existing Toolkit/Repair Kit scan-cost contract, until the coordinated V2 lifecycle is ready.
- **Scanner Charge approved in principle:** V2 uses a unique **crafted, tradable Scanner Charge** for charge-paying general fleets. It replaces Toolkit/Repair Kit scanning inputs only when Programs, SAGE Editor/converter, generated universe/config, and FC App activate the V2 contract together.
- **Recipe not approved:** Scanner Charge ingredients and quantities are **TBD pending economy approval**. No recipe in this proposal is implementation authority.
- **Data Runner direction changed:** every qualifying Data Runner scan consumes **zero Scanner Charges**, matching Starbased's unique Data Runner utility. Data Runner ownership/qualification is itself the unique scan-cost utility; other specialist benefits may remain, but cannot reintroduce a charge cost.

The implementation interpretation is compositional, not a client-selected exemption: a Data Runner-only / all-Data-Runner composed Fleet whose authoritative `scan_cost == 0` consumes zero configured cost. A mixed Fleet still pays the authoritative additive `scan_cost` contribution of every non-Data-Runner hull/config; adding one Data Runner cannot zero unrelated hull costs. Programs derives this from the Fleet and config accounts—there is no client-supplied specialist or free-scan flag.

Zero Scanner Charges does **not** mean zero opportunity cost. Data Runners still commit cooldown, time, route choice, travel fuel, cargo/fitting capacity, exposure, and the one-active-signal slot; failed or abandoned attempts still consume those opportunities.

The recommended coordinated V2 loop is:

1. **Read the map:** choose a Region and interpret visible signal conditions.
2. **Fit the fleet:** choose a pattern, general-fleet Scanner Charge supply, cargo room, and scanner-focused hull/config; qualifying Data Runners require no charges.
3. **Detect:** commit the authoritative composed charge cost—zero only for an all-Data-Runner Fleet whose `scan_cost == 0`—and advance that Fleet's one durable tracker.
4. **Move:** travel to the recovered coordinate before the signal expires.
5. **Recover:** settle the immutable resolved Contact and collect direct loot.
6. **Analyze and specialize:** use or sell materials and Data Cubes; progress pattern, Region, quality, and cadence branches.
7. **Move on:** exhausted signals and one-active-signal rules make exploration more valuable than parking.

### Coordinated V2 reward posture

- **Primary:** direct, useful cargo—materials, consumables, components, and rare research commodities.
- **Rare career artifacts:** Rare, Epic, Legendary, and Anomalous Data Cubes.
- **Not at V2 activation:** generic randomized loot boxes. No authoritative source currently commits scanning to loot boxes, while the research/data model explicitly calls for real Data Cube cargo and scan mappings.[6][13]
- **Post-V2 option:** an earned-only Encrypted Cache can be evaluated after real telemetry, but its contents must be committed at scan time, odds disclosed, and no paid key or reroll sold.

## Why this should be the V2 target

Current scanning is a single transaction, a cooldown, and a weighted cargo roll. The caller selects a pattern; Programs evaluates coordinate/time noise, chooses blank or one eligible static row, scales quantity linearly by scan power, clips it to cargo capacity, and awards flat XP.[1][2]

The five emitted patterns currently differ primarily by procedural noise field and nominal SDU amount.[3][4]

That is enough machinery for a proof of concept, but not enough player agency for a career. The player cannot read the live signal, understand actual odds, choose a semantic destination, or do anything after pressing Scan beyond waiting for cooldown.[8][9]

The dormant advanced dataset proves that loot-oriented categories have already been explored—common supplies, ores, refined materials, weapons, electronics, rare materials, titan components, and stimulants—but its 85 rows are shadowed by colliding IDs and are not release-ready.[5]

## Current state versus coordinated V2

| Area | Current / Phase 3 bridge | Recommended coordinated V2 |
|---|---|---|
| Core action | Select pattern → immediate roll | Detect → travel → recover |
| Location | Raw X/Y/time procedural noise | Authoritative Region profile + local signal target |
| Rewards | One SDU row per pattern | Direct materials/components + Data Cubes |
| Pattern choice | Mostly linear payout tiers | Five horizontal strategies with distinct reasons to choose |
| Failure | Blank result after full cost | No-contact result: lower XP, readable feedback, no full reward |
| Scan input | Existing Toolkit/Repair Kit contract can remain for Phase 3 | Crafted, tradable Scanner Charges for general fleets after coordinated activation; recipe TBD |
| Scanner ships | Data Runner scans currently have zero scan cost | An all-Data-Runner Fleet with authoritative composed `scan_cost == 0` consumes zero Scanner Charges; a mixed Fleet pays the additive non-Data-Runner contribution, with opportunity costs preserved |
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

- exact Scanner Charges derived from authoritative Fleet/config composition: `0` for an all-Data-Runner Fleet whose composed `scan_cost == 0`, otherwise the additive non-Data-Runner contribution;
- scan cooldown and expected total loop time;
- cargo room after any general-fleet charges are consumed;
- signal-quality contribution;
- bulk-yield multiplier;
- research/Region locks by player-facing node name;
- whether another unresolved signal blocks this fleet.

### 3. Detect

A scan:

- recomputes and consumes the authoritative composed Scanner Charge cost: zero only for an all-Data-Runner Fleet whose `scan_cost == 0`, while a mixed Fleet pays every additive non-Data-Runner contribution;
- resolves the fleet's Region authoritatively;
- selects the Region loot profile and chosen pattern;
- commits exact future entropy slots `+2/+6/+10` and the reward envelope;
- advances the monotonic sequence on the one durable `ScanSignal` tracker per Fleet.

Resolve then reads the three authoritative SlotHashes in order inside the configured window and stores the immutable **No Contact** receipt or Contact payload. Missing that window is a late-entropy forfeit, not a reroll.

A target signature includes category, rarity band, target coordinate/radius, expiration, and risk—not the exact reward.

### 4. Move and recover

After Resolve stores Contact, the fleet travels to the target and runs Recover before expiry. Recovery:

- verifies the same fleet is inside the radius;
- validates the immutable resolved Contact;
- deposits direct cargo using fixed or bounded scaling;
- awards the full Data Runner XP;
- records a reconnect-safe terminal receipt and local exhaustion; Acknowledge later clears only the terminal presentation payload while preserving the tracker.

Travel is the missing verb in the current loop. It creates route choice, exposure, fuel cost, ship identity, and opportunities for future encounters. Those costs, plus cooldown, time, fitting/cargo tradeoffs, and the one-signal slot, keep zero-charge Data Runner scanning from becoming a zero-opportunity-cost action.

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

### Data Cubes are not loot boxes in V2

The existing progression already defines Data Cube Analysis and Rare/Epic/Legendary/Anomalous refinement nodes.[6] A prior decision record explicitly chose real Data Cube cargo rows and scanning mappings rather than inert labels.[13]

For coordinated V2:

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

### Scanner Charge activation contract

Scanner Charges are a unique **crafted and tradable** V2 resource. Because Toolkits and Repair Kits now have repair utility, they remain available for that purpose rather than becoming the permanent general-fleet V2 scan input.

- General fleets pay the pattern/configured Scanner Charge amount after coordinated V2 activation.
- A Data Runner-only / all-Data-Runner composed Fleet whose authoritative `scan_cost == 0` consumes `0` Scanner Charges; no rounding rule or floor may change that result.
- Mixed Fleets pay the authoritative additive `scan_cost` contribution of their non-Data-Runner hulls/configs. Adding one Data Runner cannot zero unrelated hull costs.
- Programs derives the cost from authoritative Fleet/config accounts. The client supplies neither a specialist qualification flag nor a free-scan flag.
- Scanner Charges replace the current Toolkit/Repair Kit scan input only when the coordinated V2 lifecycle activates.
- **Open economy gate G1:** exact recipe ingredients and quantities are TBD pending explicit economy approval. The proposal intentionally specifies no recipe.
- Phase 3 may retain the existing scan-cost contract until that activation.

## Specialist Data Runner ships

Three current hulls are explicitly authored with `Spec: Data Runner`:

| Hull | Size | Base power | Base cooldown | Cargo | Current scan cost |
|---|---|---:|---:|---:|---:|
| Opal Rayfam | Small | 950 | 312 s | 5,640 | 0 |
| Fimbul BYOS Ranger | Medium | 1,050 | 300 s | 16,652 | 0 |
| VZUS opod | Medium | 1,100 | 300 s | 13,781 | 0 |

The hull metadata and scanning loadouts confirm the intended specialist role.[10][11][12]

### Recommended specialist contract

Data Runner hulls should combine their unique **zero-charge utility** with bounded information and cadence advantages, not an uncapped loot multiplier:

- preserve their materially shorter cooldowns and stronger Scanner Array/Scan Drone loadouts;
- `+10` normalized signal-quality score;
- `+50%` signal expiration window;
- a Data Runner hull/config contributes its authoritative zero scan cost; a Fleet composed only of such Data Runners has composed `scan_cost == 0` and consumes `0` Scanner Charges;
- one additional preview detail—category, risk modifier, or tighter target radius;
- no exclusive access to the career itself.

General ships can scan and contribute their configured charge amount. Data Runner hulls contribute zero Scanner Charges, so an all-Data-Runner Fleet whose authoritative composed `scan_cost == 0` pays zero; a mixed Fleet still pays the additive contribution of every unrelated non-Data-Runner hull/config. Data Runners still commit cooldown, travel time and fuel, route and exposure risk, fitting/cargo tradeoffs, and their one active signal, so zero charge cost is not zero opportunity cost.

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
2. **Exact future-slot commitment.** Detect commits `+2/+6/+10`; the deciding entropy must not exist when cost is committed.
3. **Immutable ordered resolution.** Resolve reads authoritative SlotHashes in order once; abandoning cannot reroll into a better item.
4. **Recovery required.** Full reward and most XP settle only at the target.
5. **Committed opportunity costs remain sunk.** General fleets lose configured charges; all fleets still spend cooldown/time and, when they pursue a contact, route fuel and exposure. A Data Runner's zero charge cost does not refund those costs.
6. **Regional signal exhaustion.** Repeated recoveries in one Region reduce rare-profile availability; movement restores opportunity.
7. **Bounded quantity modes.** Fixed discrete drops and capped square-root bulk scaling.
8. **Composed charge rule.** Programs derives cost from authoritative Fleet/config accounts. An all-Data-Runner Fleet with composed `scan_cost == 0` consumes zero; a mixed Fleet pays its additive non-Data-Runner contribution, and no client flag can make it free.
9. **Capacity-aware preflight.** The UI warns when valuable output would be clipped.
10. **Server/program authority.** Region, profile, signal, target, and reward envelope are not client-selected.
11. **Telemetry:** attempts, contacts, recoveries, expirations, abandons, reward VU, clipping, Region/pattern/hull, charge amount, Data Runner qualification, and time-to-recover.

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
- exact authoritative composed charge cost: `0` for an all-Data-Runner Fleet whose `scan_cost == 0`, otherwise the additive non-Data-Runner contribution;
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
- committed charge and opportunity costs, including a clear zero-charge Data Runner indication;
- Recover CTA;
- on recovery: exact item rows, quantities, XP, Region/pattern/hull context.

The client should stop presenting static noise-weight sums as if they were current signal and should remove stale XP-per-power copy.[8][9]

## Technical contract

### Target accounts and sidecars

- `ScanPatternPolicy`: a program-owned pattern policy sidecar for enabled lifecycle/version, profile selection, timing and entropy windows, output bounds, and the configured cost/quantity rules shared with generated clients.
- `ScanLootProfileUpload`: a bounded staging sidecar for converter-emitted profile chunks plus expected version/digest. Finalization validates chunk order, completeness, and bounds before promotion.
- `ScanLootProfile`: the bounded finalized Region-owned loot table and value budget. Programs resolves and validates it; the client cannot substitute entries or a richer profile.
- `ScanSignal` PDA: canonical seeds are **Game + Fleet**, never Character. Fixed-layout account data records Game, Owner Profile, owner/controller Character, Fleet, and required control witnesses. One tracker per Fleet therefore survives owner/controller Character changes; validated witness fields are refreshed in place rather than creating a new tracker.
- Durable `ScanSignal` state: monotonic sequence, active lifecycle data, exact entropy slots, local exhaustion, an immutable per-sequence Contact/NoContact result, and reconnect-safe terminal receipts. A used tracker cannot be closed and recreated to reset sequence or exhaustion.
- `ScanLootEntry` extension: `quantity_mode = Fixed | BulkSqrt`, rarity, category, optional research gates.
- Scanner Charge cargo/recipe/config rows: unique, crafted, and tradable; ingredient identities and quantities remain blocked on economy gate G1.
- Region profile reference in SES/converter output.

Use these sidecars rather than widening Character. FC is a direct-chain client through the generated IDL/SDK: it opens, refreshes, detects, resolves, recovers, acknowledges, and reads receipts from Programs/accounts directly. V2 adds no backend or Galaxy runtime dependency.

### Entropy contract

At Detect slot `s`, Programs commits the exact future slots `s + 2`, `s + 6`, and `s + 10` into that signal sequence. Resolve reads authoritative SlotHashes evidence for those committed slots **in order** and inside the policy's resolution window, then stores an immutable Contact or NoContact payload/receipt for the sequence. The contract does not require or claim distinct leaders; callers cannot choose replacement slots, reorder evidence, or rewrite a resolved payload.

If no valid Resolve occurs before the window closes, late entropy is an irreversible forfeit. Configured charges and opportunity costs stay spent, no recovery reward or XP is available, and the tracker records a reconnect-safe terminal forfeit receipt rather than returning to a rerollable blank state.

### Lifecycle and instructions

The state path is Open → idle, Detect → pending entropy, Resolve → Contact pending recovery or terminal NoContact, and Recover / late-entropy forfeit / Abandon / Expire → terminal receipt. Acknowledge returns the tracker to idle while preserving durable anti-reroll state.

- `OpenScanSignal`: authenticates the current controlling Profile/Character with `SCAN` permission scoped to SAGE + Fleet, validates Game/Fleet/owner/controller witnesses, and creates the canonical Game + Fleet tracker only as a virgin sequence-`0` account.
- `RefreshScanSignalWitnesses`: authenticates the current controlling Profile/Character with Fleet-scoped `SCAN` and revalidates Fleet-control witnesses after control changes, updating the fixed-layout tracker in place without changing its PDA or resetting sequence/exhaustion.
- `DetectSignal`: authenticates the current controlling Profile/Character with Fleet-scoped `SCAN`, validates idle/acknowledged state, Region, `ScanPatternPolicy`, finalized `ScanLootProfile`, research, cooldown, and Fleet composition, and binds cost consumption to that authoritative Fleet cargo. It derives additive `scan_cost` from authoritative Fleet/config accounts, consumes zero only when the all-Data-Runner composition has `scan_cost == 0`, charges mixed Fleets for every non-Data-Runner contribution, increments the monotonic sequence, and commits slots `+2/+6/+10`. It accepts no client-supplied specialist/free flag or alternate inventory recipient.
- `ResolveSignal`: permissionless and deterministic inside the configured window; it accepts no caller-selected result fields, reads the three committed authoritative SlotHashes in order, and writes the immutable per-sequence Contact or NoContact payload/receipt. It cannot swap slots or resolve the same sequence twice.
- `ForfeitScanSignalEntropy`: permissionless and deterministic after the Resolve window; it accepts no caller-selected outcome, finalizes that sequence as forfeited with no loot or recovery XP, and does not refund cost or erase the sequence.
- `RecoverSignal`: the final account contract must authenticate the current controller and stored owner/Fleet witnesses, validate the immutable Contact payload, target radius, and TTL, and bind cargo/XP settlement to those canonical recipients. It then settles bounded cargo, updates local exhaustion, and records the terminal recovery receipt. **Recover is the remaining Programs implementation dependency on the frozen Career XP sidecar ABI; its final authority/account list is still outstanding, and this proposal does not claim Recover is already implemented.**
- `AbandonSignal`: only the immutable stored owner Profile may call it, through `ProfileValidation` with `SCAN` permission scoped to SAGE + the stored Fleet; there is no controller/admin fallback or caller-selected recipient. It irreversibly terminates the active sequence without loot or recovery XP and records a terminal receipt; committed costs, cooldown, sequence, and exhaustion remain.
- `ExpireSignal`: permissionless after Contact TTL; it records a terminal expiry receipt without accepting a reward/rent recipient or making the sequence rerollable.
- `AcknowledgeScanResult`: only the immutable stored owner Profile may call it with stored-Fleet-scoped `SCAN`; no live Fleet or alternate recipient is accepted. After receipt readback it clears the terminal presentation payload but preserves the Game + Fleet authority, monotonic sequence, local exhaustion, and tracker account.
- `CloseScanSignal`: only that same authenticated stored owner Profile may close a virgin sequence-`0` tracker that has never detected, and reclaimed rent returns only to that Profile. No independent recipient or controller/admin fallback exists. Any used tracker is permanently non-closeable, so it cannot be closed/recreated to reset sequence, exhaustion, or anti-reroll history.

### Existing systems to reuse

- pattern accounts and noise maps;
- RegionTracker coordinate resolution;
- authoritative SlotHashes commit/reveal evidence;
- research tags and Data Runner modifiers;
- FC cargo-delta findings panel and direct-chain transaction flow through the generated SDK;
- SAGE Editor pattern/profile authoring and converter pipeline.

This is a coordinated **Programs + SAGE Editor/converter + generated universe/config + FC App** contract. It cannot be activated safely as a config-only shortcut. Generated outputs must come from the reviewed Editor/converter source at pinned revisions, and this proposal does not authorize automatic re-init generation, deployment, or chain mutation.

## Coordinated V2 scope and Phase 3 boundary

The overhaul may be developed during Phase 3, but it is not required to ship Phase 3. Current scanning and its existing Toolkit/Repair Kit scan cost may remain in the Phase 3 release until every V2 workstream below is ready for coordinated activation.

### Required for coordinated V2 activation

1. Direct-loot catalog and four Data Cube cargo rows.
2. Region loot profiles generated from current world data.
3. Fixed versus square-root quantity modes.
4. Durable Game + Fleet `ScanSignal` lifecycle: Open/Refresh witnesses, Detect, ordered Resolve, late-entropy forfeit, Recover, Abandon, Expire, Acknowledge, and virgin-only Close, with future-slot reveal and reconnect-safe receipts.
5. Five differentiated, staggered patterns.
6. Authoritative composed scan cost: zero for an all-Data-Runner Fleet whose `scan_cost == 0`; mixed Fleets pay additive non-Data-Runner contributions, plus any separately approved specialist bonuses.
7. FC map/chooser/findings/recovery UX.
8. Research cost migration away from SDU.
9. Exact-head converter, Rust schema, program, FC, and chain-backed integration tests.
10. Telemetry and economy budget dashboards before mainnet tuning.

The activation boundary includes Programs, SAGE Editor/converter source, reviewed generated universe/config output, and FC App behavior together. FC remains direct-chain through the generated SDK; no backend/Galaxy runtime is added. A config-only patch is insufficient, and no automatic re-init generation is implied or authorized.

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

These estimates are planning inputs for work during/after Phase 3, not a Phase 3 blocker or a promise that detailed tuning has been approved. A compressed immediate-loot version can be smaller, but it should be described honestly as a fallback—not the recommended career loop.

## Rollout gates

1. Confirm V2 product scope without making it a Phase 3 release gate.
2. Close economy gate G1 for Scanner Charge ingredient identities and quantities; do not infer a recipe from this proposal.
3. Freeze IDs and data ownership across Programs and SAGE Editor/converter.
4. Implement a feature-flagged/new-account program path; preserve legacy scanning until coordinated migration.
5. Generate current-target universe/config from the reviewed SAGE Editor/converter source into isolated output; prove unrelated sections unchanged. Do not use a config-only shortcut or automatic re-init generation.
6. Run deterministic economic simulation across every hull/config and mixed-Fleet composition, Region, pattern, rarity, and cargo-cap boundary, including all-Data-Runner `scan_cost == 0` and additive non-Data-Runner charge cases.
7. Run lifecycle/commit-reveal adversarial tests: wrong Open/Refresh witnesses, late entropy, slot reordering/substitution, replay, wrong Fleet, wrong Region/profile, stale SlotHashes, abandon/reroll, close/recreate after use, reconnect before Acknowledge, full cargo, insufficient mixed-Fleet charges, and all-Data-Runner zero-cost authority.
8. Deploy the exact Programs/IDL/SDK + SAGE Editor/converter + generated universe/config + FC App pair to a test cluster.
9. Run a populated FC walkthrough with specialist and general hulls, screenshots, console, and transaction evidence.
10. Read back every pattern/profile and sample signal/reward account.
11. Tune via telemetry; no mainnet activation until economy and security sign off separately.

## Decision record

Michael Wagner's 2026-08-25 direction resolves or changes the product-contract questions below. The only open executive-disposition gate is the Scanner Charge recipe; detailed balance remains proposal material, not approved implementation values.

| # | Disposition | Decision | Owner |
|---|---|---|---|
| E1 | **Resolved — direction approved, timing changed** | Develop Detect → Travel → Recover during/after Phase 3; do not make it a hard Phase 3 blocker. | Executive + Product + Programs + FC |
| E2 | **Resolved** | Phase 3 may ship current scanning and its existing Toolkit/Repair Kit scan cost unchanged until coordinated V2 activation. | Product + Release |
| E3 | **Resolved** | V2 Scanner Charges are unique, crafted, and tradable; they replace general-fleet Toolkit/Repair Kit scan inputs only at coordinated activation. | Executive + Economy + Programs + SAGE Editor + FC |
| E4 | **Changed** | Qualifying Data Runner scans consume zero Scanner Charges, matching Starbased's unique Data Runner utility. Data Runner ownership/qualification is the unique scan-cost utility; other specialist benefits cannot contradict it. | Executive + Ships + Economy + Programs |
| G1 | **OPEN ECONOMY GATE** | Approve exact Scanner Charge recipe ingredients and quantities. This proposal supplies none. | Economy |

The contact chances, rarity mixes, pattern unlock levels, loop times, VU budgets, 10/52 bridge XP, detailed loot rows, and implementation estimates elsewhere in this proposal are **not approved by this executive disposition**. They remain explicit tuning assumptions for their named owners to validate separately.

## Known unknowns

- **Open economy gate G1:** exact Scanner Charge recipe ingredients and quantities require explicit economy approval; none are specified here.
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

No live config, generated universe/config, deployment, automatic re-init generation, or chain write was performed.
