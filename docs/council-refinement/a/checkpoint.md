# Lane A checkpoint — Targeting runtime/interface reconciliation

**Task:** `targeting-runtime-reconcile`
**Captured:** 2026-10-01T14:24:41Z
**Disposition:** **BLOCKED** — positive-tier source mechanics are coherent, but binary compatibility, fixture, public SDK, and exact-target gates are not closed.
**Production change:** none. The producer branches remain owned by `pinchy-SA`; no write handoff was provided.

This checkpoint is a source/layout/interface assessment. It is **not** E2E proof, release approval, migration approval, deployment authorization, or a cutover-ready claim.

## 1. Immutable identities and live state

| Source | Exact identity | Live status at capture |
|---|---|---|
| Planning PR [sage-editor #274](https://github.com/staratlasmeta/sage-editor/pull/274) | `f7ea917661c384ee48905615d7d453ca1c9cda18` | open draft, mergeable, review required, no human reviews, CodeQL green |
| Programs [#1042](https://github.com/staratlasmeta/programs/pull/1042) | `4ee78371521df9ecfe0fae926f5f4201881d07a6` | open draft, mergeable, review required, no human reviews/comments, three failed checks |
| Programs PR base | `9676a9f0a16186443fa86d141d3112762dc704cd` | merge base with current main |
| Programs current `main` | `aeaf1a08206cc7caa5e34b3774f0099e050a0702` | three commits ahead of PR base |
| Editor [#272](https://github.com/staratlasmeta/sage-editor/pull/272) | `80678b0f10b438fe2ae8924fa20e0dbea245115f` | open draft, mergeable, review required, no human reviews/comments, policy-source checks red |
| Editor current `master` | `9fcf4d2b254d917a8ee933ce4ea6898a3b2a9b2c` | PR base/current master |

The supplied Editor witness `43e4cc9dffec1d10001640c61efcffa6c5f22c1c` was stale. The current head `80678b0f…` adds the ATLAS-unit labeling correction and its test updates.

Planning file identities:

- `ACTIVE-WAVE.md`: SHA-256 `d96752e3c94317770969950ca1dfc71c54a84b57a9bd082fe023dfbba2ec7cd8`
- `active-wave.json`: SHA-256 `92770e80f040b3a4e1a824fd882963c3ac4cde7fd1d706367b87102b3f6f19a1`

Programs source tree: `8605b1359ce3345d9b07103bdb0fd1c794f5af90`.

Machine-readable identities are in [`source-identities.json`](source-identities.json).

## 2. Targeting-authored versus current-base work

Programs #1042 contains two authored commits:

1. `7475a1f175fd658513f09c9a162b9f716cb09522` — runtime, schema, mechanics, migration note.
2. `4ee78371521df9ecfe0fae926f5f4201881d07a6` — generated IDL/TS/Rust interfaces and fixture-constructor updates.

Current Programs `main` advanced through #1035, #1037, and #1038. The Targeting PR is two commits ahead and three commits behind current main. Current-base overlap is limited to:

- `clients/packages/sage/idl.json`
- `tools/sage-blackbox-tests/tests/player_flows/xp_building_ledger.rs`

A read-only `git merge-tree` showed no conflict markers, but the overlap remains semantically relevant because current main regenerated genesis fixtures without the Targeting field. No synthetic current-main build/test was run.

No Targeting source path was silently inherited from those three current-main commits. The runtime and interface changes assessed here are the two commits above.

## 3. Runtime contract at Programs `4ee783715…`

### Modifier and research sync

- `CharacterModifier.hit_chance_modifier` is `PackedValue<I32F32>`.
- Default/raw base is zero.
- `CharacterModifier::combine` adds the lane.
- partial C4 schema input defaults the field to `0.0`.
- each config node is range-validated to `[-1.0, +1.0]`, while aggregate Character values may exceed one node's range.

### Hit-chance calculation order

1. The existing ship/size pipeline calculates Q6 `PreciseStatVal` hit chance.
2. That base lane is clamped to `[0.05, 1.0]`.
3. The Q6 value is converted to integer PPM by multiplying by `1,000,000` and flooring.
4. The Character's raw I32F32 modifier is scaled directly to signed PPM using `i128` and integer division, truncating toward zero.
5. Signed PPM is saturating-added to the floored base threshold.
6. The final threshold is clamped to `[0, 1,000,000]`.

Observed positive tiers:

- zero tiers: `0` modifier PPM;
- +0.01: `+10,000` PPM;
- +0.04: `+40,000` PPM;
- representative zero-tier base: `843,750` PPM, exactly matching the legacy threshold.

### Combatant ownership

- attacker fire reads the attacking fleet's `character`;
- defender counterfire reads `defender_character`;
- the AttackFleet instruction already carried and validated both Character accounts, so instruction account order and discriminator are unchanged;
- starbase attack remains a hard-coded `1,000,000` PPM and never reads the Targeting modifier.

### Roll and telemetry parity

`CombatAttackOutcome.hit_chance_ppm` is the single source for:

- `roll_against_threshold_ppm`;
- `CombatActionSummary.hit_chance_ppm`;
- `ShotSummary.hit_chance_ppm`.

At zero bonus this equals the legacy Q6-derived threshold. Telemetry schema remains v3; no event field or record-length change was introduced.

### Unsupported negative semantics

Negative values execute mechanically but are not an approved product rule:

- `-0.01` converts to `-10,000` PPM through truncation toward zero;
- because the modifier is added after the 5% base floor, a sufficiently negative value can take the final threshold below 5%, down to the final clamp at zero;
- the current tests pin only the `-0.01` conversion mirror, not a negative gameplay policy.

No negative-policy redesign is proposed. One source comment says the conversion uses an arithmetic shift/floor; the implementation actually uses signed division/truncation toward zero. The producer should correct that documentation without changing this wave's behavior.

## 4. Exact serialized layout

Executable probes compiled the PR base and exact PR head in separate target directories. All listed sized types had alignment 1.

### Fixed-sized portions

| Type | Base `9676a9f…` | Head `4ee783715…` | Delta |
|---|---:|---:|---:|
| `CharacterModifierSized` | 99 | 107 | **+8** |
| `CharacterSized` | 282 | 282 | 0 |
| `CharacterModifiersSized` | 6 | 6 | 0 |
| `CharacterSyncSized` | 78 | 78 | 0 |
| `ResearchNodeSized` | 82 | 82 | 0 |
| `ResearchTreeDefinitionsSized` | 4 | 4 | 0 |
| `GameSized` | 342 | 342 | 0 |

Within `CharacterModifierSized`:

- existing `scan_cool_down_modifier`: offset 91;
- new `hit_chance_modifier`: offsets **99–106**;
- old `research_tags` tail start: 99;
- new `research_tags` tail start: 107.

### Representative unsized payloads

These sizes exclude an outer program-account discriminator.

| Payload | Base | Head | Delta |
|---|---:|---:|---:|
| empty `CharacterModifier` | 111 | 119 | +8 |
| default `Character` | 407 | 415 | +8 |
| default `CharacterSync` | 189 | 197 | +8 |
| default `ResearchNode` | 205 | 213 | +8 |
| one-node `ResearchTreeDefinitions` | 227 | 235 | +8 |

Relative payload offsets:

- `Character`: nested modifier starts at 296; new field is 395–402; tags move 395 → 403.
- `CharacterSync`: modifier starts at 78; new field is 177–184; tags move 177 → 185.
- `ResearchNode`: modifier starts at 94; new field is 193–200; tags move 193 → 201.

For complete Character/CharacterSync account data, add the 8-byte account discriminator to those offsets.

The migration document's claim that the Character sized header grows four bytes is incorrect. `CharacterSized` is unchanged; the nested modifier payload grows eight bytes.

## 5. Demonstrated old-byte incompatibility

The migration document says pre-upgrade accounts fail closed. That is true for some values, but false for the research tree/Game path.

Old bytes were serialized by exact base `9676a9f…` and decoded at exact head `4ee783715…`:

| Old bytes decoded by new Rust layout | Observed result |
|---|---|
| empty `CharacterModifier` | `RawSliceAdvance` failure |
| default `Character` | `RawSliceAdvance` failure |
| default `CharacterSync` | `RawSliceAdvance` failure |
| one-node `ResearchTreeDefinitions` | **success with `nodes=0`** |
| checked-in genesis Game fixture | **success, but node count changes 63 → 0** |

The exact same `fixtures/game-genesis.bin` is 2,532,230 bytes:

- base Rust decoder: 63 research nodes;
- head Rust decoder: 0 research nodes;
- head generated TypeScript decoder in CI: rejects with `Codec [u16] expected 2 bytes, got 1`.

For the same semantic 63 nodes, the field alone adds `63 × 8 = 504` bytes, before any new Editor nodes. The expected same-content raw length would therefore be 2,532,734 bytes, but D must generate and verify the real selected artifact rather than synthesize it from this calculation.

**Conclusion:** old Game/ResearchTree bytes can be silently accepted with the research tree erased. Existing-game incompatibility is a hard deployment exclusion, not merely a migration TODO. A fresh-genesis candidate requires freshly serialized Game bytes from the exact selected Programs and Editor sources.

## 6. Generated interface boundary

IDL semantic comparison against the PR base found:

Changed:

- `characterModifier`
- `characterModifierSized`

Unchanged top-level objects that link to the changed type:

- `character`
- `characterSync`
- `characterModifiers`
- `researchNode`
- `researchTreeDefinitions`
- `game`
- `attackFleet` instruction ABI

The unchanged outer account objects do **not** imply wire compatibility.

Pinned outputs:

- IDL raw SHA-256: `b12c198ebd27a77914892fabfd3fcc71608cbbeb62ee3ce993572a2aec126629`
- Targeting semantic IDL SHA-256: `add0996d764e7250380aec53cff4f47f25f46d3182595deb0e61ce2371a23603`
- TS `characterModifier.ts`: `7e37ad756c0945472c508e83ddf6e417ad14c7e66b0906048f3f3401a123aa98`
- TS `characterModifierSized.ts`: `d7e0c1047dd6864e03091a092c5557a624477374154bfa931a298f9ae8e8e140`
- Rust SDK modifier: `889147a00b4e05ec49987fd0fb0b116ff2605ac3336c78b4e01c2a91d32c3f28`
- Rust decoder modifier: `1fe75a6f158d7e75e0f63e2d52d2aa3580b47f583995459e6d7f96a795a924b3`

### Public package refusal for C

The currently published `@staratlas/dev-sage@0.53.0` tarball has SHA-256 `947e46ff3b64ecd4c7fced788a7881d23f26283b3686e1056b7f654e699c8adf` and contains neither the field nor its IDL entry. The branch still declares package version `0.53.0`.

C must **not** select or guess a package version. Until a new package is published and pinned, it must use an exact generated artifact from the selected Programs commit or remain BLOCKED. A dependency resolving to published `0.53.0` is explicitly incompatible with this candidate.

No SBF binary, deployed program, release package, or target Game identity was supplied or produced by Lane A. Binary/deployment identity remains **NOT PROVIDED**.

## 7. Telemetry decoder contract for C

Fleet-vs-fleet telemetry remains Borsh schema v3:

- kind: `1`;
- version: `3`;
- complete record length: 468 bytes;
- attacker `ShotSummary` offset: 228;
- defender/counterfire `ShotSummary` offset: 336;
- each `ShotSummary`: 108 bytes;
- `hit_chance_ppm`: little-endian `u32` at shot-relative offset 0.

`ShotSummary` relative layout:

| Field | Offset | Size |
|---|---:|---:|
| `hit_chance_ppm` | 0 | 4 |
| `dodge_chance_ppm` | 4 | 4 |
| `attempted` | 8 | 1 |
| `hit` | 9 | 1 |
| `dodged` | 10 | 1 |
| `crit` | 11 | 1 |
| `raw_damage` | 12 | 8 |
| `blocked_damage` | 20 | 8 |
| `effective_damage` | 28 | 8 |
| `effective_damage_by_type` | 36 | 64 |
| `other_effective_damage` | 100 | 8 |

C must:

1. require exact kind/version/length and reject truncation/trailing bytes;
2. ignore transactions with `meta.err != null`;
3. treat each shot's `hit_chance_ppm` as the exact threshold actually rolled;
4. never recompute the Targeting bonus from the legacy Q6 chance;
5. require D's exact program/Game/generated-interface identity before mounting the Targeting path;
6. refuse published SDK `0.53.0` and any old Game target rather than guessing compatibility.

## 8. Commands and observed local results

Exact-source worktree: `/root/staratlas/programs-worktrees/targeting-schema-4ee78371` at detached `4ee783715…`.
Base probe worktree: `/root/staratlas/programs-worktrees/targeting-base-9676` at detached `9676a9f…`.
Both were clean after temporary probes were removed.

### Layout probes

```text
CARGO_TARGET_DIR=/root/staratlas/targets/targeting-base-layout \
  cargo test -p sage_star_frame --test targeting_layout_probe -- --nocapture
```

Result: **PASS**, 1 test. Produced the base sizes and 63-node Game witness.

```text
CARGO_TARGET_DIR=/root/staratlas/targets/targeting-head-layout \
  cargo test -p sage_star_frame --test targeting_layout_probe -- --nocapture
```

Result: **PASS**, 1 test. Produced head sizes and cross-version decode outcomes. The probe was temporary assessment code and was removed; it is not represented as committed regression coverage.

### Focused Targeting/runtime tests

```text
cargo test -p sage_star_frame --lib hit_chance -- --nocapture
```

Result: **PASS**, 5 tests; 992 filtered out.

Individually executed and **PASS**:

- `test_attack_outcome_reports_bonus_ppm_for_attacker_and_defender_retaliation`
- `test_starbase_attack_outcome_takes_no_bonus`
- `unsized_test_character_modifier_update_and_combine`
- `unsized_test_sync_with_tree_unions_categories_and_resets`

```text
cargo test -p c4_schema
```

Result: **PASS**, 31 tests; 0 failures.

```text
cargo fmt --all -- --check
git diff --check
```

Result: **PASS** after temporary probes were removed.

Not run locally:

- full `cargo test -p sage_star_frame --lib`;
- `cargo check --workspace --all-targets`;
- `cargo clippy -p sage_star_frame --lib -- -D warnings`;
- local client install/build/typecheck/full tests;
- SBF build, validator, fixture refresh, blackbox journey, or live transaction.

The corresponding exact-head CI successes are evidence for #1042, but they are not claimed as local executions.

## 9. Exact-head CI evidence

### Programs #1042

Green exact-head checks include Rust programs/build/decoder/lint/doc/fmt/test/C4 schema and TS build/typecheck/lint/fmt/generation.

Failed exact-head checks:

1. `rust / blackbox-tests`
   - fixture fingerprint stale;
   - recorded inputs hash `9fac3dd79bab139e94a2b8192e3a489c9b98b20b03fae29e708e5b162153ef7d`;
   - computed `aa7f2ea399234602f6b757db3fd622050f64f8838d7bacba208f73c089637714`.
2. `ts / test`
   - 103 passed, 1 failed;
   - the generated TS Game decoder rejects the old genesis bytes with `Codec [u16] expected 2 bytes, got 1`.
3. `rust / combat-sbf-v0`
   - three combat telemetry tests fail during Character registration;
   - stale bytes produce `RawSliceAdvance` and custom error 2002.

### Editor #272

Failed exact-head gates remain:

- `research-nodes` / `research-nodes-macos`: frozen Crafting/Council policy-source boundary mismatch;
- `resource-atlas` / `resource-atlas-macos`: policy-source SHA mismatch.

These are separate from routine generated freshness and remain owner/policy gates.

## 10. Readiness verdict

### What is supported

- The approved positive Targeting mechanic is source-coherent.
- zero-base additive sync, +1pp/+4pp conversion, per-side Character selection, roll/telemetry parity, final cap, and starbase exclusion are locally green in focused host tests.
- generated IDL, TS, Rust SDK, and Rust decoder sources contain the field at exact head.

### What is not supported

- existing-game upgrade or migration;
- any claim that old accounts universally fail closed;
- use of published TS SDK `0.53.0`;
- exact deployed binary or target identity;
- fresh-genesis fixture readiness;
- real nonzero purchase → sync → attack/counterfire E2E;
- release/cutover readiness;
- negative-modifier product policy.

No production repair was authored because the producer retains #1042 and no explicit handoff exists.

## 11. Immutable handoffs

### To D

Use Programs `4ee783715…`, Editor `80678b0f…`, and plan `f7ea91766…`. Do not reuse or restamp the old Game bytes. Generate fresh selected Game/genesis bytes, assert the complete expected node set including #469–472, decode the exact output with both Rust and TS interfaces, then run real nonzero purchase → sync → attacker/counterfire and exact telemetry assertions. Do not infer readiness from host tests or a fingerprint-only update.

### To C

Use the telemetry contract in §7. Treat SDK/package/target identity as a hard capability gate. Published `@staratlas/dev-sage@0.53.0` is incompatible. Require D's exact program binary, Game account, IDL, and generated-client identity; refuse old targets. `hit_chance_ppm` is authoritative and must not be reconstructed from Q6.

## 12. Anchored follow-up proposal and stop gate

Ownership is unresolved, so this lane stops at assessment. The bounded producer-coordinated follow-up is:

1. correct `TARGETING-HIT-CHANCE-MIGRATION.md`:
   - nested +8-byte change, not a +4 Character header;
   - Character/CharacterSync fail closed, but ResearchTree/Game can silently decode as an empty tree;
   - generated clients are present at the current head;
2. commit a raw old-byte regression proving the ResearchTree/Game behavior cannot silently collapse 63 nodes to zero, or introduce an explicit reviewed layout-generation refusal;
3. keep live migration and negative-policy design excluded from this wave;
4. rerun focused host tests, generated TS/Rust decoder tests, fresh fixtures, and exact-head CI after the owner-selected repair.

**One precise resume action:** after an explicit handoff from `pinchy-SA`, add the raw old-Game/ResearchTree refusal regression at the then-current #1042 head; otherwise wait for D's fresh-genesis bytes and rerun Rust + generated TS decoding against that immutable artifact without modifying producer source.

## 13. Operational note

The host began at 100% disk use. To permit isolated builds, only reproducible build outputs were removed from inactive old worktrees (`tools/sage-blackbox-tests/target` and an old `target-zink`); source, `.git`, fixtures, branches, and dependency manifests were not deleted. Free space rose to approximately 29 GiB before the focused builds.
