# C4 Scanning — Final Proposition (2026-09-04)

**Program · SAGE Editor · FC App — one loop, three repos, one activation gate.**

> **Status:** Final revision of the scanning proposition (supersedes `kingler-audit-docs/c4-scanning-release-proposal-20260824.md` as the working target; the executive disposition recorded there is unchanged and restated in §1).
> **Written:** 2026-09-04 by Kingler, verified against code at the heads below. Numbers marked *tuning* are proposal assumptions, not approved runtime configuration.
> **Baselines:** programs `main` `9c90a4c96` (Phase 3 re-init baseline `6be6d4d2e`) · sage-editor `master` `12000a737` (regen head `d706a5a`) · star-atlas-tech `main` `f51acc8c1` · Phase 3 program `4LSpiEtN5EwXkL79KbrtwZj4C4TnEWEjaPDTDCDQG7M1`.
> **Related:** [VPS handoff](https://github.com/jfloyd959/claude-brain/blob/main/wiki/star-atlas/c4-scanning-career-xp-vps-handoff-20260902.md) · [Phase 3 receipt](https://github.com/jfloyd959/claude-brain/blob/main/star-atlas/phase3-reinit-rollout-receipt-v2-2026-09-03.md) · [programs#947](https://github.com/staratlasmeta/programs/pull/947) · [sage-editor#237](https://github.com/staratlasmeta/sage-editor/pull/237) · [sage-editor#242](https://github.com/staratlasmeta/sage-editor/pull/242) · [kingler-audit-docs#1](https://github.com/kingler959/kingler-audit-docs/pull/1).

---

## 0. Decision sheet — rule these and the rest is execution

| # | Decision | Recommendation | Owner | Blocks |
|---|---|---|---|---|
| **D1** | How `RecoverSignal` awards its 52 Data Runner XP while the Career XP sidecar ABI is unfinished | **Land it on the legacy `Character.xp_info.collect_xp` path now** — identical to legacy `Scan`, Crafting, Combat, Pilot, Building and to `ResolveSignal`'s own 10-XP No-Contact award already in #947. programs#920 exists precisely to rewire every gameplay XP hook through the sidecars in one regen; Recover joins that sweep like the rest. No client XP/decay argument, no mutable-policy reread (Rev 15 still holds). | Joseph + Programs (Jacob) | **Everything downstream: P6 → P7 → P8 → P9 → FC** |
| **D2** | 12 of 32 catalog rows (8 exotic/legendary items + 4 Data Cubes) require `minimum_risk: High`; the 69-Region map has **0** High-risk Regions | Author High-risk Regions in the Map Editor for the exotic/legendary 8 (this is what "Deep Space Scanning L18" and "Enemy Faction Scanning L22" are for) **and** re-rate Rare/Epic Data Cubes to `Medium` so the cube research chain is reachable before High-risk access. Legendary/Anomalous cubes stay High. | Design (map) + Econ (Chris) | S3 re-derivation, S5 |
| **D3** | Every one of the 69 generated Region profiles carries the *same* four resource rows (Carbon, Copper Ore, Iron Ore, Silica) | Re-derive Region rows from the resource map that merged to master today (sage-editor#236, `codex/resource-map-economy-balance`) so Regions differ by what is actually mined there. Without this, "read the map" has nothing to read. | Joseph (SES/converter) | S3′ |
| **D4** | Deployment shape for V2 | **Program upgrade of the Phase 3 program, no wipe.** V2 is additive (18 new instructions, 4 new account types, legacy `Scan` untouched, 0 diff lines). Policies/profiles are created by `init-game` reconciliation; `ScanSignal` trackers are created per fleet by players. Legacy scanning keeps working until FC hides it. | Programs deploy authority + Joseph | Rollout §9 |
| **D5** | `ResolveSignal` must run inside 256 slots (~100–130 s) of Detect or the signal is forfeited with cost sunk | FC auto-submits Resolve ~5 s after Detect confirms, **and** Star Atlas runs a permissionless keeper for Resolve / Forfeit / Expire (all three are designed permissionless). A player who closes the tab must not lose a paid scan. | Joseph (FC) + infra | F4, ops |
| **D6** | Scanner Charge recipe (economy gate G1) | Still open, still **not** an activation dependency (Rev 7: initial V2 keeps Repair Kit cost rows; swapping token 3 → 13188 later is config-only). Park it; do not let it block. | Econ (Chris) | nothing |
| **D7** | Ship fun improvements on the live Phase 3 loop *now*, with zero program change | Approve the bridge track (§8): honest pattern launcher, "signal here now" from the on-chain noise maps, cargo-clip preview. Same components V2 reuses. | Joseph (FC) | B2–B4 |

Rule D1 and the V2 critical path opens today. Everything else can be ruled in parallel.

---

## 1. Executive summary

**What players have today (Phase 3, released 2026-09-04):** legacy V1 scanning — pick a pattern, pay one Repair Kit, get an immediate weighted roll against a loot table gated by procedural noise at your coordinate, cooldown, done. With sage-editor#242 (ready for review, coupled to Chris's `storage_cost` pass) that roll draws from 85 authored rows / 74 distinct items instead of SDU-only. The engine already does location × pattern × threshold × weighted roll; it just had one row per pattern.

**What the spec asks for (executive-approved direction, Michael Wagner 2026-08-25):** an *exploration-and-recovery career* — **Read the map → Fit the fleet → Detect → Move → Recover → Analyze/specialize → Move on.** Detect commits cost and future entropy; Resolve fixes an immutable Contact with a target coordinate, category and rarity band; the fleet travels; Recover settles direct loot and most of the XP at the target. Tradable Data Cubes replace SDU as the career commodity. Not a Phase 3 blocker; developed during/after Phase 3; activated across all three repos together.

**What is built:** more than the thread implied.

| Layer | Built | Missing |
|---|---|---|
| Programs (programs#947, draft, 31 commits, CI 21/22, now CONFLICTING vs today's main) | P1–P5D: 4 accounts, 18 instructions, `[+2,+6,+10]` SlotHashes entropy, deterministic Contact/NoContact, generic multi-cargo cost, Region/research/focus gates, exhaustion, Abandon/Expire/Acknowledge/Close, tombstones. 72 + 99 + 822 tests. Generated clients regenerated (most of P8). | `RecoverSignal` (blocked on **D1**), P7 c4-schema/c4-cli, P9 blackbox, rebase |
| SAGE Editor (sage-editor#237, draft, 13 commits, MERGEABLE) | S1–S3B3: reserved IDs (13188, 13189–13192, recipe 5917), 5 policies, 32-row catalog, 69 deterministic Region profiles with Q6 anchors, hashing, desired-state artifact — all deliberately disconnected from canonical output | S3′ (**D3**), S4 canonical patterns, S5 research/SDU migration, S6 ship parity, S7 converter sections + readiness record, S8 configurator, S9 validation |
| FC App (star-atlas-tech) | Nothing. A pinned file manifest exists (§7). | F1–F9, all of it |
| Career XP (#919/#920/#5342) | c5a/c5b committed on the VPS only; F7e0 885 KB uncommitted; F7e–F7l unbuilt | An ABI that, per Rev 15, gates Recover — hence **D1** |

**The recommendation in one paragraph:** rule D1 so `RecoverSignal` lands on the same XP path every other gameplay instruction uses today; finish P6–P9 and rebase #947; connect the SES artifacts behind the `scan_v2` readiness record after re-deriving Region rows from the new resource map and fixing High-risk reachability; build FC from the pinned manifest with a confirmation-aware phase executor and auto-Resolve; deploy as an additive program upgrade plus `init-game` reconciliation (no wipe); activate when all three are proven on a test cluster with a populated walkthrough. Meanwhile ship the bridge track on the live Phase 3 loop so scanning is honest and readable before V2 arrives. Re-baselined effort: **18–23 AI-days** across the three repos plus review, earliest activation **3–4 weeks after D1**.

---

## 2. The loop, and why it is fun

Fun here means: every step gives the player a *decision*, the outcome is *readable*, the risk is *chosen*, and the payoff feeds something they care about. V1 fails on all four after the button press; V2 is designed around them.

| Step | Player decision | Tension | Payoff | What breaks it |
|---|---|---|---|---|
| **1. Read the map** | Which Region, at what risk, for which category mix | Risk × distance × exhaustion | A route worth flying | Regions that all look the same (**D3**), no High-risk anywhere (**D2**) |
| **2. Fit the fleet** | Pattern (five *different* strategies), cargo room, Data Runner (free) vs general (charge), research locks | Cooldown/time vs yield; clipping | Feeling of expertise; specialist identity | Hidden costs, locked rows hidden instead of explained, "R-104" instead of a node name |
| **3. Detect** | Commit: cost + one-active-signal slot + future entropy | Sunk cost; the dice are cast before you can see them | Anticipation (commit/reveal) | Forfeit because a tab closed (**D5**) |
| **4. Move** | Fly to the target before TTL; route/fuel/exposure | Clock vs distance; PvP exposure | Space is space again; ship speed matters | TTL shorter than intra-Region travel; no route CTA |
| **5. Recover** | Inside the radius, before expiry | Last-moment failure modes | Direct, useful cargo + 52 XP; readable receipt | Cargo silently clipped; XP not settled at recovery |
| **6. Analyze / specialize** | Sell, craft, or research with cubes; which branch next | Career vs economy tradeoff (higher patterns pay more VU, less XP/h) | Progression that changes decisions at 8/15/25/38 | SDU-in-disguise; cube gating its own first drop |
| **7. Move on** | Stay and exhaust, or relocate | Exhaustion meter vs travel cost | Exploration beats parking | Invisible exhaustion; no reset feedback |

V1 today delivers step 2 (partly) and the "Recover" payoff collapsed into the same click as Detect — no travel, no target, blank result after full cost, exact loot printed on the card before you scan. The bridge track (§8) fixes readability inside V1; only V2 adds steps 3–5 and 7.

---

## 3. Where we are, precisely

### 3.1 Phase 3 bridge (live)

- Engine: `scan.rs` — eligible rows `threshold < base_value + scan_bonus` (noise at coordinate × time) ∧ research gates; roll over `blank_weight + Σ roll_weight`; `amount = output_amount × effective_scan_power`; `saturating_emit` clips to hold via `storage_cost`; XP flat per outcome; cooldown = base × pattern multiplier × research.
- Loot: sage-editor#242 replaces each pattern's single SDU row with the 85 authored rows (rows only; noise, cost, cooldown, blank unchanged). 74 outputs: 58 crafted items, 16 raw ores + SDU. Amount scale: ship `scan_power` raw 360–2,610 (median 720) multiplies every row, so **1/PWR rows yield ≥ 360 per hit** unless the hold clips. Resolution (Joseph, 2026-09-04): Chris authors a `storage_cost` pass across all cargo types (all = 1 today) and #242 ships coupled to it; clamp = `floor(free_capacity / storage_cost)`; hold capacity p10 389 / p50 17,341 / p90 828,682; R4 consumable rows still need `output_amount` edits.
- Receipt: `scanning_patterns` row flipped to CHANGED, awaiting owner signature. Post-launch loot edits reconcile in place via `UpdateScanPattern.loot_table` — never a wipe.
- Known V1 limits that no data fix reaches: no travel, no commit/reveal (latest slot hash), exact loot disclosed pre-scan, `scan_bonus` authored 0 on all 2,928 configs, SDU still the research currency.

### 3.2 Programs — V2 on programs#947

- Accounts: `ScanSignal` (536 B, PDA Game + Fleet, owner/controller witnesses in header, monotonic `sequence`, exhaustion history, immutable Contact payload, terminal receipts), `ScanPatternPolicy` (Game + PatternId: strategy, `contact_chance_bps`, `max_rarity`, required tags, `target_radius`, `signal_ttl_secs`, XP 10/52, exhaustion, `value_budget`, `allowed_focus_category_mask`), `ScanLootProfile` (Game + RegionId: `risk_value_multiplier_bps`, ≤ 32 anchors, ≤ 64 rows), `ScanLootProfileUpload` (staged chunks).
- Instructions (18): Open, RefreshWitnesses, Detect, Resolve, ForfeitEntropy · Abandon, Expire, Acknowledge, Close · policy Create/Update/Remove · profile Create/Update/Remove · upload Start/Append/Cancel. Discriminants are an additive tail; Recover appends without shifting any.
- Behaviour: Detect derives Region from `RegionTracker` (lowest id on overlap, deep space rejected), gates on Region + policy research (controller Character), computes the eligibility bitmap (pattern bit, focus, row research, `max_rarity`, `value_units ≤ floor(value_budget × risk_multiplier)`), consumes `ceil(scan_cost × multiplier)` per cost row (zero rows when composed `scan_cost == 0`), stores reveal slots `commit + [2,6,10]`. Resolve is permissionless inside `[commit+10, commit+10+256)`, reads the exact SlotHashes, one `Pcg64Mcg` stream, rejection sampler; NoContact awards 10 XP (legacy path) and clears; Contact copies cargo/rarity/mode/category/row/base/nominal/XP/target/radius/expiry/decay/seed. Exhaustion decays deterministically and resets on Region change.
- Status: draft; CI 21/22 (only `blackbox-tests` fixture freshness, not a required check); **CONFLICTING** against today's main (main has moved past the `6be6d4d2e` baseline; the latest landing is starbase governance v1, #731) — needs a rebase.
- Missing: `RecoverSignal` (math done: P5A raw-bit radius, P5B immutable decay), P7, P9.

### 3.3 SAGE Editor — V2 on sage-editor#237

- `scan_v2_pattern_policies.json`: Broad/Focused/Enhanced/Deep/Spatial — contact 85/80/72/65/50 %, TTL 30/34/40/48/64 min, radius 1.0/0.8/0.65/0.5/0.35, max rarity Rare/Epic/Legendary/Legendary/Anomalous, value budget 10/14/22/38/80, exhaustion 400/500/650/800/1000 bps per recovery (max 5000, decay 30 min), unlock tags 104 · 106 · 107+20 · 105+102 = research nodes **Focused Array Patterns**, **Enhanced Signal Patterns**, **Deep Resonance Patterns + High Risk Zone Access**, **Spatial Anomaly Patterns + Anomalous Data Cubes**. Focused focus mask = Industrial | Technology | Tactical.
- `scan_v2_loot_catalog.json`: 32 rows. Common/Uncommon materials and consumables on Broad/Focused (BulkSqrt), Technology components on Focused/Enhanced (Fixed), exotic/titan/legendary + cubes on Deep/Spatial (Fixed, weights 0.03–0.8). Cubes carry row research gates 99–102.
- `scan_v2_region_profiles.json`: 69 Regions, 4–8 anchors each (system galactic coordinates, Q6), 15 Low / 54 Medium / 0 High, and **identical resource rows everywhere** (**D3**).
- `scan_v2_economy.json`: Scanner Charge 13188 + four cubes as cargo types; no recipe (G1).
- Isolation: everything under `src/future/` + `artifacts/future/`; two tests assert the generator is *not* in `package.json`. Do not "fix" that.

### 3.4 FC App — nothing built, seams pinned

Current fc-app (`packages/fc-app`): pattern cards render on-chain `lootTable` with exact items and XP; `handleScan` submits one `Scan`, then infers findings from a cargo-hold delta ~15 s later; a mock `/scanResult` route exists; blocked patterns are filtered out rather than explained; research locks render as `R-<tag>`. The manifest in §7 pins every file to modify/create.

### 3.5 Career XP — the dependency that D1 removes from the critical path

Every XP-awarding instruction on `main` today calls `Character.xp_info.collect_xp` directly: `scan.rs`, `complete_crafting_process.rs`, combat, Pilot (movement), Building (claim stakes + habs), DailyXp, `grant_xp`. programs#920 ("settle C4 career XP through gameplay hooks", 100 files) rewires exactly those — including `scan` — through the sidecars in one regenerated client surface. `ResolveSignal` in #947 already awards No-Contact XP on that legacy path with a 6-account list frozen by test. Holding only `RecoverSignal` back for an ABI that #920 will apply to all of them is inconsistent and parks V2 behind an offchain proof system (F7e–F7l) with no ETA. Hence D1.

---

## 4. Gap analysis against the spec — by loop step and repo

| Step | Programs | SAGE Editor | FC App |
|---|---|---|---|
| Read the map | Region + profile authority ✅ | Region profiles ✅ but undifferentiated (**D3**), no High risk (**D2**) | Climate overlay ❌ (F6) |
| Fit the fleet | Composed cost, research/focus gates ✅ | Policies ✅, research stagger ❌ (S5), ship parity check ❌ (S6) | Launcher/preflight ❌ (F3, F7) |
| Detect | ✅ | Readiness record ❌ (S7) | Phase executor ❌ (F4, F5), auto-Resolve ❌ (**D5**) |
| Move | Movement settlement in Recover ❌ (P6) | — | Route-to-target via planner witness ❌ (F5) |
| Recover | **`RecoverSignal` ❌ (D1 → P6)** | — | Findings from durable receipt ❌ (F8) |
| Analyze / specialize | — | SDU → cube/component research costs ❌ (S5), cube nodes must not self-gate | Named locks, progression copy ❌ (F3/F7) |
| Move on | Exhaustion ✅ | Exhaustion tuning (policy) ✅ | Exhaustion meter ❌ (F6/F7) |
| Cross-cutting | P7 config/CLI ❌, P8 regen (redo after Recover), P9 blackbox ❌ | S4 canonical set, S8 configurator, S9 validation ❌ | F1 SDK packing, F2 accounts, F9 tests/preview ❌ |

---

## 5. Programs plan (P6–P9) — `staratlasmeta/programs`, branch `sage/c4-scanning-v2-p1-p5d-20260902` → continue on it

### P0 — Rebase #947 onto `main` (`9c90a4c96`)
Conflicts are expected only in root instruction registration and generated clients; regenerate clients rather than merge them (decision 1 of the handoff). Re-run the CI commands, not a narrower local gate: `cargo clippy --all-features --all-targets`, `cargo test --features idl`, `pnpm run generate` diff checks.

### P6 — `RecoverSignal` (after D1)
**Args:** `key_index: u16`, `expected_sequence: u64`. No XP, decay, quantity, target or recipient argument of any kind.
**Accounts:** `profile_validation` (current controller, `SCAN` scoped to SAGE + stored Fleet), `game`, `fleet: Mut<ValidatedFleet>` (settle any completed move through the existing `update_state` projection with the Character witness, then read authoritative coordinates), `owner_profile` + `owner_character` (stored witnesses, read-only), `controller_character: Mut` (XP recipient, same as Resolve), `scan_signal: Mut<Seeded<…>>`. No policy or profile account: Recover consumes only the immutable Contact payload (Rev 2B).
**Logic, in order:** status == `Contact` ∧ `sequence == expected` → witnesses match → `now < expires_at` → movement settled, fleet Idle → `distance² ≤ target_radius²` over raw `I8F56` bits (P5A helper) → cargo-category gate (same `ensure_cargo_allowed` as legacy Scan) → `saturating_emit(nominal_quantity, cargo_type, capacity)`; `accepted = hold delta`, `clipped = nominal − accepted` written to the receipt → `collect_xp(DataRunner, reward_xp)` on the controller Character (**D1**) → `ScanSignal::recover(...)` updates `last_region`, `consecutive_recoveries`, `last_recovery_at` with the stored `exhaustion_decay_secs`, sets `Recovered`, `terminal_at` → cooldown untouched (it was set at Detect).
**Tests (unit + instruction):** replay after Recovered; wrong fleet/owner/controller; outside radius by one raw bit; exact boundary inside; expired by one second; unsettled movement rejected; Fixed ignores power; BulkSqrt nominal from the Detect snapshot; full hold → accepted 0, clipped = nominal, XP still awarded, receipt correct; exhaustion increments and resets on Region change; XP account list frozen by the same structural test Resolve uses (6 accounts, no `Option<`/`Rest<`).

### P7 — `c4-schema` + `c4-cli` reconciliation
- `config-schemas/c4-schema/src/scanning_v2.rs`: sections `scanning_pattern_policies` (5 rows, keyed by pattern id) and `scanning_loot_profiles` (≤ 69, keyed by region id) with the exact field set of §3.2, raw fixed-point encodings, and status.
- `cli/c4-cli/src/init_game/{scan_pattern_policy,scan_loot_profile}.rs`: create / revision-checked update / remove (tombstone) per Rev 10; profiles through Start/Append/Create-or-Update staged upload.
- Dependency DAG (Rev 2F): cargo + research → map/RegionTracker + legacy patterns → policies → profiles → **decoded semantic readback** of every policy/profile (a successful tx is not convergence).
- `validate-config`: preflight the Rev 12 bounds (≤ 512 nodes, ≤ 4,096 provider tags, ≤ 4 Region requirements, ≤ 4 per row), anchor-in-polygon, cargo existence, pattern mask ⊆ 0..4, `BulkSqrt` base bounds.
- Reminder: `validate-config` takes the config as stdin/JSON text, not a path.

### P8 — regenerate IDL / TS / Rust SDK / decoder after Recover lands
Canonical scripts only; never hand-edit. Expose `ScanSignalStatus` as a real enum (today `status` is a bare `u8` in the IDL) so FC gets a typed union.

### P9 — blackbox player flows (`tools/sage-blackbox-tests/tests/player_flows/scanning_v2.rs`)
Matrix from the plan: open→detect→resolve miss; open→detect→resolve contact→move-in-radius→recover; wrong owner/fleet/Game/Region/profile/policy; revision drift; missing tags/charges; early/exact/stale/missing-hash entropy; outside radius/expired/replay; abandon + permissionless expiry; Fixed/BulkSqrt/capacity boundaries; exhaustion decay/reset; legacy `Scan` + `EncounterCommit` coexistence. Regenerate the fixture through `refresh-fixture.sh` with a real `solana-test-validator` (a maintainer-side step; not on the VPS).

### Two program risks to close in the same pass
- `signal_ttl_secs` is validated only `> 0`: add an upper bound (e.g. 24 h) so an authoring mistake cannot brick a fleet's scanning (Acknowledge and Expire both gate on `expires_at`).
- Rev J's sidecar ruling must bind Resolve and Recover identically after D1, so #920's restack changes both in one place.

---

## 6. SAGE Editor plan (S3′–S9) — `staratlasmeta/sage-editor`, continue on `sage/c4-scanning-v2-ses-20260902`

- **S0 — refresh** onto `master` `12000a737` (the branch was cut from an older master; #236 resource-map economy balance merged today and must be in the base for S3′).
- **S3′ — Region rows from the resource map (D3).** Replace the current uniform 4-row derivation with per-Region body-resource membership from the merged resource-map economy balance: rank by richness/occurrence with stable cargo-id tie-breaks, cap deterministically, then add the economy-owned global rows (components, cubes) by risk/category rules; stay within 64 rows / 32 anchors. Prove: every Region differs from at least one neighbour; every cargo exists; every row has ≥ 1 pattern bit.
- **S2′ — reachability (D2).** Author High-risk Regions in `Map Editor` (or accept the design's chosen alternative) and re-rate Rare/Epic cubes to Medium. Test: every catalog row appears in ≥ 1 generated profile; every research-gated row's gate node does not itself cost that row's cargo.
- **S4 — one canonical five-pattern set.** Keep pattern ids 0..4 and the Repair Kit cost rows (token 3 × 1) as the V2 activation cost (Rev 7). Retire the default/advanced ID shadowing: after #242 the advanced file is archival — mark it non-emitting explicitly.
- **S5 — progression.** Place the five pattern nodes at Data Runner 0 / 8 / 15 / 25 (+ High Risk Zone Access) / 38 (+ Anomalous Data Cubes). Replace SDU costs on Data Cube Analysis, Rare/Epic/Legendary/Anomalous refinement, Signal Amplification and Rapid Cycling with the component/cube chain in the proposal; preserve node ids; run the research cargo-cycle and starter-bootstrap tests. SDU stays a Phase 3 bridge drop and is retired at V2 activation, not before.
- **S6 — ship parity.** Prove all 144 Data Runner configs remain `scan_cost = 0` with positive scan power and all general scanners positive integer cost; composed all-Data-Runner fleets = 0, mixed = Σ non-Data-Runner. Author `scan_bonus` on scanner hulls (it is 0 on all 2,928 configs and absent from the ship SoT).
- **S7 — converter root sections + the readiness record (Rev 2G).** One exact-target `scan_v2` record: Programs schema/deployment id, IDL/SDK version, FC support, economy sign-off, cluster. Missing/disabled → byte-identical legacy contract; enabled-but-incomplete → **abort before writing**; complete → emit `scanning_pattern_policies`, `scanning_loot_profiles`, cubes, research overrides, pattern costs, ship changes together. Unrelated sections byte-for-byte unchanged (the receipt's section-diff proves it).
- **S8 — Scanning Configurator.** Truthful previews: policy per strategy, Region profile/category/risk view, Fixed vs BulkSqrt accepted quantity with the `storage_cost` clip, named research gates, radius/TTL/contact, canonical vs archival labels. Remove XP-per-power and static-noise probability copy.
- **S9 — validate.** typecheck/build/tests, isolated full emit, Rust `validate-config` at the exact Programs head, Research Nodes sync/graph tests, ID registry invariants (recheck 13188–13192 / 5917 against open PRs immediately before commit), ship parity, browser tests. No promotion into Programs, no re-init.

---

## 7. FC App plan (F1–F9) — `staratlasmeta/star-atlas-tech`, `packages/fc-app`

**Modify:** `config/accountRegistry.ts` (register `ScanSignal` with the compile-time `owner_profile` offset, `requireProfile: true`), `stores/DataStore.tsx`, `stores/RpcDataStore.tsx` (profile-accessor resource; **no** global subscription runner; targeted PDA reads only), `actions/FleetActions.ts` (one adapter per phase; replace the duplicate legacy `scan`/`scanFleet`), `components/PixiMap/FleetInfoPanel.tsx` + `.module.css` (launcher always enterable; no exact-item disclosure before recovery; one scroll owner), `components/PixiMap/PixiMap.tsx` (remove `PendingScanObservation`, cargo-delta findings and legacy `handleScan`; wire signals, executor, receipts, layer, climate, route), `surfaceScanFailure.ts` (typed outcomes), `movementPlanning.ts` + `movementPlannerState.ts` (optional immutable scan-signal witness on `MovementDestination`).
**Create:** `scanning/types.ts`, `scanning/scanSignalRepository.ts`, `scanning/scanPhaseExecutor.ts`, `scanning/scanProjection.ts`, `scanning/scanAvailability.ts`, `hooks/useScanSignals.ts`, `components/PixiMap/ScanLauncher.tsx` + css, `components/PixiMap/ScanSignalLayer.ts`.

- **F1** — consume the generated `@staratlas/dev-sage` from a packed exact-branch artifact; PR stays draft until the package publishes; then pin the released version.
- **F2** — accounts: `ScanPatternPolicy`, `ScanLootProfile`, profile-filtered `ScanSignal` (memcmp on the fixed offset) + direct Game+Fleet PDA derivation for the connected profile's fleets. Never subscribe to all signals.
- **F3** — pure adapters: status projection; policy/profile joins; authoritative Region; **named** research gates (node names, never `R-104`); generic cost rows × composed `scan_cost` with an explicit zero-charge Data Runner indication; quality/TTL/radius previews; Fixed/BulkSqrt nominal **and** cargo-capped output; exhaustion presentation; consolidated five-row identity.
- **F4** — phase executor for Open / Detect / Resolve / Recover / Abandon / Expire / Acknowledge: pre-fetch Game+Fleet+signal, validate owner/sequence/status, submit, then post-confirm fetch and prove **both** sequence and status. Outcomes exactly `confirmed | definitive_failure | confirmation_unknown | confirmed_but_projection_stale`; unknown never triggers an optimistic next phase or a blind retry. **Auto-Resolve** ~5 s after Detect confirms (D5), retried inside the window, with the keeper as backstop.
- **F5** — lifecycle: Open on first use; Detect → "Analyzing"; Resolve → No Contact feedback or Contact target; reopen active state from chain on reconnect; route to target through the shared planner with the signal-sequence witness; Recover enabled only inside the radius; Abandon with consequences shown (no cooldown or lockout shortcut); Acknowledge clears the receipt.
- **F6** — map: Region signal climate (risk band, dominant categories from the profile rows, exhaustion), unresolved-signal marker with TTL, target marker + radius + route. Retained Pixi layer with event-driven `reconcile()`; no per-frame account transforms; inactive signals allocate nothing.
- **F7** — launcher: exactly five horizontal strategy rows, each with purpose/unlock, exact cost, actual cooldown, contact chance and rarity ceiling, Region category mix, quality/yield/TTL/radius effects, nominal vs capped output warning, named locks, active-signal blocker. **Blocked rows stay visible with the reason.** One scroll owner; row five reachable at desktop, mobile width and short height.
- **F8** — findings from the durable receipt only: Pending / No Contact / Contact / Expired / Recovered. Contact shows category, rarity band, target, radius, TTL, committed cost. Recovered shows exact rows, accepted vs clipped, XP, Region/pattern/fleet. Retire the mock `/scanResult` route.
- **F9** — tests (manifest list in the pinned FC manifest: registry offset ±1, per-phase account parsing, executor outcome matrix incl. status-only/sequence-only fixtures, projection leak tests, availability copy, launcher reachability mutations, layer zero-ops, movement witness preservation), typecheck, lint, production build, exact-head preview, populated walkthrough with a Data Runner and a general hull, screenshots and console check. No chain → hard blocker reported, not mocked.

---

## 8. Bridge track — fun on the live Phase 3 loop, zero program change (D7)

These use today's on-chain data and become the V1 adapter of the V2 components above.

- **B1 (in flight)** — sage-editor#242 + Chris's `storage_cost` pass; R4 rows re-amounted. Receipt signature.
- **B2 — honest launcher (F7-lite).** Same `ScanLauncher` component with a V1 data adapter: real cost (pattern cost rows × fleet `scan_cost`, Data Runner shows 0), real cooldown, named research locks, cargo-clip preview `min(output × power, floor(free / storage_cost))`, all rows visible with reasons. Stop printing the full loot table with XP on the card; show category mix and rarity ceiling instead.
- **B3 — "signal here, now".** The V1 signal *is* the on-chain noise field, and it is public and deterministic: `base_value(coordinate, time)` from the `ScanPattern.noise_maps` the client already fetches. Evaluate it client-side with bit-exact parity (build the program's `get_scan_value` to WASM from the same crate, or an exact JS port validated against the Rust vectors) and show per pattern a **weak / stable / strong / volatile** band at the fleet's position (three timestamps → volatility) plus a coarse per-Region heat sample. This is the spec's "read the map" step, delivered on V1 data, and it replaces the static noise-weight sums the proposal criticised. Measured today: SDU-row eligibility spans 2–15 % of the map by pattern, so players are currently flying blind.
- **B4 — findings.** Keep the cargo-delta panel (V1 has no receipt) but only after the transaction confirms, label it as inferred, and delete the mock `/scanResult` route.
- **Not in the bridge:** cost token changes, SDU retirement, any program instruction.

---

## 9. Rollout, gates and the activation boundary

1. **Rulings** D1–D7 (§0).
2. **Programs:** P0 rebase → P6 → P7 → P8 → P9 → flip #947 to ready → human review (1 approval, 18 required contexts; blackbox not required) → merge → **program upgrade** of `4LSpiEtN5EwXkL79KbrtwZj4C4TnEWEjaPDTDCDQG7M1` (additive; legacy `Scan` untouched) → publish `@staratlas/dev-sage`.
3. **SAGE Editor:** S0 → S3′/S2′ → S4–S9 → flip #237 → review → merge. Readiness record marked complete for the target cluster only when 2 is deployed and 4 is merged.
4. **FC:** F1–F9 on the packed SDK → walkthrough on a test cluster → published SDK pin → review → merge. Client activates V2 UI when the Game's policies/profiles exist on chain and hides legacy Scan; otherwise it stays on the bridge UI.
5. **Config apply:** converter emit with the complete readiness record → `c4-cli validate-config` (stdin) at the exact Programs head → `init-game` reconciliation creates/updates policies and profiles (no section scoping exists; the receipt's section diff proves nothing else moved) → decoded readback of every policy/profile.
6. **Gates before activation** (from the plan, unchanged): pre-flight rebases; frozen IDL/client SHA + SES artifact hash; SES output passes the exact Rust schema; unrelated `universe.json` sections byte-identical; adversarial commit/reveal/replay/wrong-account/stale-revision/expiry/cargo-cap/abandon tests; deterministic economy matrix across every hull/config × Region × pattern × rarity × cap boundary within approved VU envelopes; FC built against the packed then published SDK; chain-backed populated Detect→Resolve→Move→Recover evidence; coordinated PRs with cross-links.
7. **Post-activation:** telemetry (attempts, contacts, recoveries, expirations, abandons, VU, clipping, Region/pattern/hull, charge amount, Data Runner qualification, time-to-recover) before any mainnet tuning; Scanner Charge (G1) flips cost rows 3 → 13188 by config when Econ approves.

**No wipe at any step.** Phase 3 was the wipe; V2 accounts are new PDAs; ScanSignal trackers are player-created; policy/profile edits are revisioned in-place updates.

---

## 10. Effort, re-baselined (AI-assisted days; human review extra)

| Workstream | Original estimate | Done | Remaining |
|---|---:|---|---:|
| Programs (P0 rebase, P6, P7, P8 redo, P9, TTL bound) | 6–8 | P1–P5D, most of P8 | **4–5** |
| SAGE Editor (S0, S3′, S2′, S4–S9) | 2–3 + 3–4 | S1–S3B3 | **4–5** |
| FC App (F1–F9) | 4–6 | manifest only | **6–8** |
| Integration, security, economy, chain-backed walkthrough | 4–5 | — | **4–5** |
| **Total** | 19–26 | | **18–23** |

Critical path: D1 → P6 (2 d) → P7/P8 (1.5 d) → SDK publish → F1–F9 (6–8 d, can start on the packed artifact the day P8 lands) → integration (4–5 d). Earliest activation ≈ 3–4 weeks after D1, assuming review turnaround measured in days. Bridge track B2–B4: 3–4 days, independent, can start today.

---

## 11. Risks and anti-fun hazards

| Hazard | Effect | Mitigation |
|---|---|---|
| Resolve window is 256 slots after `commit + 10` (~100–130 s) | Closed tab = forfeited scan, cost sunk, no reroll | Auto-Resolve in FC + permissionless keeper (D5); copy: "Analyzing… do not close" is *not* acceptable as the only defence |
| Contact TTL vs travel | 30–64 min TTL against 6–32 min intra-Region trips; slow general hulls at the edge | Anchors are systems inside the same Region; the spec's Data Runner +50 % TTL is **not visibly wired** in #947 (no TTL modifier in the Detect snapshot) — add it in P6 or drop it from the spec; FC shows ETA vs TTL before Detect and warns on a Detect it cannot make in time (advisory, not on-chain) |
| One active signal per fleet | Feels punishing if the blocker is invisible | Blocker inline in the launcher with Abandon/Acknowledge CTA and its cost spelled out |
| Exhaustion | Invisible → "the game is cheating" | Meter on the fleet card and Region climate; reset feedback on Region change |
| Cargo clipping | Silent loss of value | Preflight nominal vs accepted; receipt records clipped; Chris's `storage_cost` pass is the economic lever |
| Chain transparency | Exact reward derivable from the stored seed by a tool | Accepted and documented; official UI hides it until Recover; VRF is a separate design |
| Scanning competes with crafting | 58 of 74 Phase 3 outputs are crafted items; V2 catalog drops Steel, Electronics, cores | Per-Region value budgets, Fixed quantities for components, econ allowlists; Chris owns the envelope |
| Undifferentiated Regions (D3) / unreachable High rows (D2) | "Read the map" has nothing to read; Deep/Spatial patterns pay nothing new | S3′ + S2′ before the readiness record is marked complete |
| #947 drift | CONFLICTING today; every day of delay adds regen churn | P0 rebase first, regenerate clients, never hand-merge |
| Career XP restack later widens Resolve/Recover accounts | Second client regen + FC adapter change | Isolated per-phase adapters in `FleetActions.ts`; D1 makes the change uniform across all XP hooks |
| `signal_ttl_secs` unbounded | Authoring typo bricks a fleet | Upper bound in P6 pass; SES validator mirrors it |
| XP-v1 raw ship-count budget | Many-small-ship fleets out-train a specialist | Stays a separate, disabled decision gate |

---

## 12. Definition of done

- **Programs:** #947 rebased, `RecoverSignal` merged with the D1 path, P7 sections + DAG + readback, regenerated clients with a typed status enum, P9 flows green including the fixture refreshed by a maintainer; program upgraded on the Phase 3 program id; `dev-sage` published.
- **SAGE Editor:** #237 merged; Regions differ by resource; every catalog row reachable; five staggered pattern nodes; SDU removed from research costs at activation; readiness record complete for the cluster; converter emits V2 sections with unrelated sections byte-identical; configurator truthful.
- **FC App:** launcher, climate, lifecycle, findings, movement witness, executor outcomes, auto-Resolve; all F9 tests; populated walkthrough with a Data Runner and a general hull; legacy Scan hidden when V2 is live.
- **Integrated:** a fresh wallet opens a tracker, detects in a Medium-risk Region with Broad Spectrum, auto-resolves, sees Contact, routes, recovers inside the radius, sees the receipt with accepted/clipped/XP, acknowledges, and cannot reroll, replay or close the used tracker — proven on a test cluster with transaction evidence.
- **Bridge (independent):** #242 + `storage_cost` live; launcher honest; "signal now" bands visible; mock route gone.

---

## Appendix A — V2 instruction reference (18 on #947 + Recover)

| Instruction | Who | Args | Effect |
|---|---|---|---|
| `OpenScanSignal` | controller w/ `SCAN` | `key_index` | Create virgin Game+Fleet tracker, sequence 0 |
| `RefreshScanSignalWitnesses` | controller | `key_index` | Refresh owner/controller witnesses in place after control changes |
| `DetectSignal` | controller | `key_index, expected_sequence, scan_pattern_id, expected_policy_revision, expected_profile_revision, focus` | Gates, cost, bitmap, reveal slots, `PendingEntropy` |
| `ResolveSignal` | permissionless | `expected_sequence` | Reads 3 exact SlotHashes; `NoContact` (+10 XP) or immutable `Contact` |
| `ForfeitScanSignalEntropy` | permissionless | `expected_sequence` | Late `PendingEntropy` → zero-reward terminal receipt |
| **`RecoverSignal`** (P6) | controller | `key_index, expected_sequence` | Radius/TTL check, cargo, 52 XP, exhaustion, `Recovered` |
| `AbandonSignal` | stored owner | `key_index, expected_sequence` | Terminal, no reward; cooldown/expiry lockout kept |
| `ExpireSignal` | permissionless | `expected_sequence` | Contact TTL expiry receipt |
| `AcknowledgeScanResult` | stored owner | `key_index, expected_sequence` | Clears receipt payload; keeps sequence/exhaustion |
| `CloseScanSignal` | stored owner | `key_index` | Virgin-only rent reclaim |
| Policy `Create/Update/Remove` · Profile `Create/Update/Remove` · Upload `Start/Append/Cancel` | `MANAGE_SCANNING` | desired-state payloads, revisions | Revisioned config with durable tombstones |

Status machine: `Empty → PendingEntropy → Contact → Recovered | Abandoned | Expired`, or `PendingEntropy → NoContact`, then `Acknowledge → Empty` (sequence and exhaustion preserved).

## Appendix B — data contract, SES → chain

| SES source | Chain field |
|---|---|
| policy `strategy`, `contact_chance_bps`, `max_rarity`, `required_tags[]`, `target_radius`, `signal_ttl_seconds`, `xp.{no_contact,recovery}`, `exhaustion.{per_recovery,maximum,decay_seconds}`, `value_budget`, `allowed_focus_categories[]` | `ScanPatternPolicy.{strategy, contact_chance_bps, max_rarity, required_research_tags, target_radius (I8F56), signal_ttl_secs, no_contact_xp, recovery_xp, exhaustion_per_recovery_bps, max_exhaustion_bps, exhaustion_decay_secs, value_budget, allowed_focus_category_mask}` |
| catalog row `cargo_id, base_quantity, roll_weight, value_units, quantity_mode, rarity, program_category, allowed_pattern_ids[], research_requirements[]` | `ScanProfileLootEntry.{cargo_id, base_quantity, roll_weight (U16F16), value_units, quantity_mode, rarity, category, pattern_mask, research_requirements[≤4]}` |
| region profile `region_id, risk_value_multiplier_bps, polygon.anchors[].{x_q6,y_q6}, resource_rows + global rows` | `ScanLootProfile.{region_id, risk_value_multiplier_bps, anchors[≤32] (Q6 → Coordinate), loot_rows[≤64]}` |
| Region `scanning_research_requirements` (already on `Region`) | Detect gate on the controller Character |
| legacy pattern `cost[]` (token 3 × 1) | `DetectSignal` cost plan (Rev 7) — Scanner Charge later by config |

## Appendix C — Phase 3 bridge facts carried from #242

85 rows / 74 outputs; 58 crafted, 16 raw + SDU; eligibility % at thresholds 0.1/0.3/0.5/0.8/1.0 — Broad 49/27/15/5/2 · Focused 63/41/27/15/11 · Enhanced 52/29/21/15/12 · Deep 37/25/21/17/15 · Spatial 15/11/9/8/8; SDU (T=1) eligible on 2–15 % of the map; all 3,258 baseline cargo types `storage_cost = 1`; capacity p10 389 / p50 17,341 / p90 828,682 / max 33.2 M, 949 configs < 5,000; `scan_bonus` 0 everywhere.

## Appendix D — sources verified for this revision

programs `main` `9c90a4c96` (`scan.rs`, `scan_pattern.rs`, `xp.rs`, all `collect_xp` call sites); programs#947 head `be78ccb` (`scanning_v2.rs`, `detect_signal.rs`, `resolve_signal.rs`, scanning `mod.rs`); programs#919/#920/#5342 live state; sage-editor#237 head (`scan_v2_pattern_policies.json`, `scan_v2_loot_catalog.json`, `scan_v2_economy.json`, `artifacts/future/scan_v2_region_profiles.json`); `research_nodes-careercombatspread.json` (nodes 34/60/62/63/159/160); star-atlas-tech `packages/fc-app` (`FleetInfoPanel.tsx`, `PixiMap.tsx`, `FleetActions.ts`, `scanPatternCosts.ts`, `accountRegistry.ts`, `mockData/ScanResultData.ts`); VPS reports `c4-scanning-cross-repo-implementation-plan-2026-08-25.md` (Rev 2–17), `c4-scanning-fc-manifest-2026-08-25.md`, `c4-career-xp-and-scanning-execution-board-2026-08-28.md`; `kingler-audit-docs` release proposal `8d437202`.
