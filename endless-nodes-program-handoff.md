# Endless Research Nodes — Program-Side Handoff

**Star Atlas · C4 Progression**
**Date:** 2026-07-09
**Author:** Kingler (AI) for Joseph Floyd
**Audience:** Jacob (program team), bravetarget, bunthius
**Status:** Handoff — needs program-side input on D1–D3

---

## How to respond

1. Open the rendered doc: https://kingler959.github.io/kingler-audit-docs/endless-nodes-program-handoff.html
2. Scroll to **Section 6 — Decision Record**.
3. For each item, pick a verdict from the dropdown and add rationale.
4. Click **Export** → choose Markdown or JSON.
5. Send the file back to Joseph.

Responses stay in your browser until you export — no login, no GitHub editing.

---

## 1. TL;DR

C4 progression needs **endless research nodes** (unlimited-level prestige tracks) for Mining and Building careers. The data pipeline already supports them (`max_level` + `cost_growth_bps` fields exist in the on-chain `ResearchNode` struct and are wired through the c4-converter as of 2026-07-08). What's missing is a **per-level diminishing-returns curve on the CVC effect** — the current `combine_repeated` path applies the same modifier N times with no tapering.

**The ask:** three options for closing that gap, ranging from "ship as-is, no program work" to "add a new field + account migration." We need Jacob's call on which path to take before we can populate the endless node payloads.

---

## 2. Background — what endless nodes are

Endless nodes are research nodes with `max_level: 0` (unlimited). Each level applies the node's `CharacterModifier` payload one additional time via `combine_repeated(modifier, level)`. Players pay escalating costs (linear via `cost_growth_bps`) to keep advancing.

**Planned endless nodes (from the Mining/Building redesign proposal):**

| Node | Career | CVC | Combine rule | L10 effect | L20 effect | Curve |
|------|--------|-----|-------------|-----------|-----------|-------|
| #82 Rare Mineral Discoveries | Mining | `rare_mineral_discovery` | **multiplicative** (×1.05/level) | ×1.63 | ×2.65 | exponential (accelerating) |
| #377 Deep Vein Extraction (new) | Mining | `rare_mineral_discovery` | multiplicative (×1.03/level) | ×1.34 | ×1.81 | exponential |
| #137 Master Construction | Building | `max_productive_plots` / `max_residential_plots` | **additive** (+1 each) | +10 | +20 | linear |
| #378 Industrial Throughput (new) | Building | `crafting_efficiency_modifier` | additive (+0.01) | +10% | +20% | linear (capped at +100%) |

Full design specs are in `sage-editor/SAGE Editor Suite/Research Nodes/MINING-BUILDING-TREE-REDESIGN-PROPOSAL.md`.

---

## 3. The issue — no native diminishing returns on effect

### What IS supported: linear cost scaling per level

`research.rs:232-249` implements `scaled_cost`:

```rust
pub fn scaled_cost(&self, base_cost: u64, current_level: u32) -> Result<u64> {
    let growth = u128::from(self.cost_growth_bps)
        .checked_mul(u128::from(current_level))?;
    let scale_bps = 10_000u128 + growth;  // 10k bps = 1.0×
    (base_cost × scale_bps) / 10_000
}
```

With `cost_growth_bps = 1000` (+10% per level):

| Level | Cost multiplier |
|-------|----------------|
| L0→L1 | ×1.00 (base) |
| L1→L2 | ×1.10 |
| L10→L11 | ×2.00 |
| L20→L21 | ×3.00 |

**This is linear (additive) scaling**, not compounding. Each level costs more than the last, but the *delta* between consecutive levels is constant. That's rising cost — which reads as "diminishing value per ATLAS" from the player's perspective.

**What this can't do:** True exponential cost compounding (×1.10 each level, so L20 = ×6.7, L50 = ×117). The formula is strictly `base × (1 + bps × level / 10000)`.

### What is NOT supported: per-level tapering of the CVC effect

The modifier combine is hard-coded in `research.rs:92-137`:

```rust
pub fn combine_repeated(&mut self, other: &CharacterModifier, times: u32) -> Result<()> {
    for _ in 0..times {
        self.combine(other)?;  // unconditional
    }
    Ok(())
}
```

`combine` itself applies each field with a fixed rule:

- **Additive** for `fleet_size`, `fleet_concurrency`, `crafting_efficiency_modifier`, `max_productive_plots`, etc. — `self.field += other.field`
- **Multiplicative** for `rare_mineral_discovery` — `*existing *= *amount` (line 118)
- **Max()** for `max_ship_size`, `security_zone_access`

These combination rules are fixed in the program binary. There is no field on `ResearchNode` or `CharacterModifier` that says "this CVC applies with diminishing returns per level." To get tapering, you'd have to edit `combine_repeated` or `combine` in `programs/sage`.

### Why this matters

The 4 planned endless nodes currently exhibit two *opposite* pathologies:

- **#82 / #377 (Mining)** — multiplicative stacking gives **accelerating** returns per level. Higher levels = more value per research. Anti-pattern for prestige; rewards early whale grind and inflates late-game resource supply.
- **#137 / #378 (Building)** — additive stacking gives **constant** value per level. Less broken, but flat. No prestige feel.

Neither has the classic "each level gives a smaller marginal bonus" curve that makes endless prestige in games like EVE or OSRS feel like a grind rather than a runaway.

---

## 4. Three options for closing the gap

### Option A — Ship as-is, rely on linear cost scaling (zero program work)

**Mechanism:** Set `cost_growth_bps` in the 1000–1500 range per the proposal. Player pays ×2 at L10, ×3 at L20 for the same constant bonus. The "diminishing returns" are purely on the cost side — the bonus itself doesn't taper, but the ATLAS/XP/resource cost per marginal bonus point grows linearly.

**Pros:**
- Zero program changes — ships Monday
- Uses only fields that already exist on `ResearchNode` and are already wired through the converter
- Tunable post-launch by tweaking `cost_growth_bps` in the SoT (no migration)

**Cons:**
- Multiplicative CVCs (#82, #377) still give accelerating returns. A L20 miner is pulling ×2.65 yield per swing for ×3 cost — still a good deal for a whale.
- Additive CVCs (#137, #378) have flat marginal value. No prestige curve, just a slot grind.
- Doesn't match the "diminishing returns" fantasy players expect from prestige tracks.

**Effort:** 0 days program work. Data-only in sage-editor.

### Option B — Data-only mitigation via tuned CVC payloads (zero program work, hacky)

**Mechanism:** For multiplicative CVCs (#82, #377), set per-cargo values **below 1.0** — e.g., `diamond: 0.97` instead of `1.05`. Each level *reduces* yield by 3% multiplicatively. This is technically not diminishing returns (it's accelerating loss), but it inverts the curve — higher levels give *less* yield, which is the opposite of a prestige bonus.

**Pros:**
- Zero program changes
- Uses existing `rare_mineral_discovery` multiplicative semantics

**Cons:**
- **Wrong direction** — this models a penalty, not a prestige bonus. Useless for #82/#377.
- For additive CVCs (#137, #378): no way to taper per level. The combine is `+=`. Hard stop.
- **Not viable.** Listed only for completeness.

**Effort:** N/A — don't do this.

### Option C — Program change: add `level_penalty_bps` field (proper fix)

**Mechanism:** Add a new field to `ResearchNode` alongside `cost_growth_bps`:

```rust
pub struct ResearchNode {
    // ...existing fields...
    pub max_level: u32,
    pub cost_growth_bps: u32,
    /// NEW: Per-level penalty (basis points) applied to the modifier before
    /// combine_repeated. 0 = no penalty (current behavior). 500 = each level
    /// applies the modifier at 95% of the previous level's strength.
    pub level_penalty_bps: u32,
    // ...
}
```

Then modify `combine_repeated` to scale the modifier down before stacking:

```rust
pub fn combine_repeated(&mut self, other: &CharacterModifier, times: u32, penalty_bps: u32) -> Result<()> {
    let mut current = other.clone();
    let penalty_scale = 10_000u128 - u128::from(penalty_bps);
    for _ in 0..times {
        self.combine(&current)?;
        // Apply penalty to `current` for next iteration
        current = current.scaled_by(penalty_scale / 10_000)?;
    }
    Ok(())
}
```

This requires a `CharacterModifier::scaled_by` helper that multiplies all numeric fields by a scalar. The math for additive fields is simple; for multiplicative `rare_mineral_discovery` it compounds naturally.

**Pros:**
- Clean, proper fix — per-node tunable diminishing returns curve
- Handles both multiplicative (#82, #377) and additive (#137, #378) CVCs
- Data-only tuning post-launch: each endless node sets its own `level_penalty_bps`
- Backwards compatible: `level_penalty_bps: 0` reproduces current behavior

**Cons:**
- **Program change** — touches `ResearchNode` account layout (account migration)
- New field needs to flow through `UpdateResearchNodeInput`, the `update_node` instruction, the IDL, the c4-converter schema, the SoT JSON format, and the editor
- Account migration: existing deployed `ResearchNode` accounts need realloc / reallocation. Account size changes.
- Schema break: `c4-cli validate-config` will reject configs without the new field unless we make it optional with a default of 0
- Estimated effort: **1–2 weeks program work + migration**. Blocks Monday deploy.

**Effort:** ~1–2 weeks. Not a Monday blocker if we ship Option A first and follow up with C as a v1.5 balance pass.

---

## 5. Worked example — what each option produces

Assuming `cost_growth_bps = 1000` (linear +10%/level) and a `diamond: 1.05` CVC on node #82 (base 100M ATLAS, base ×1.05 yield):

| Level | Option A (cost scales, effect accelerates) | Option C (cost scales, effect tapers 5%/level) |
|-------|---------------------------------------------|------------------------------------------------|
| L1 | 100M ATLAS, ×1.05 yield | 100M ATLAS, ×1.05 yield |
| L5 | 140M ATLAS, ×1.28 yield | 140M ATLAS, ×1.23 yield (penalty kicks in) |
| L10 | 190M ATLAS, ×1.63 yield | 190M ATLAS, ×1.39 yield |
| L20 | 290M ATLAS, ×2.65 yield | 290M ATLAS, ×1.59 yield |
| L50 | 590M ATLAS, ×11.5 yield | 590M ATLAS, ×1.69 yield (asymptote) |

**Observation:** Option C's asymptote is the point where the penalty fully cancels the multiplicative bonus — L50 yield is ~×1.69 and barely climbing. That's the classic prestige curve. Option A keeps climbing forever, which is either "endless" in the fun sense or "runaway inflation" depending on your view.

---

## 6. Decision Record

> **Workflow:** Fill in the interactive form on the [rendered HTML page](https://kingler959.github.io/kingler-audit-docs/endless-nodes-program-handoff.html) — pick a verdict from each dropdown, add your rationale, then click **Export** to download a Markdown or JSON file. Send the file back to Joseph.
>
> Verdict values: **Accept** · **Change** · **Defer** · **Needs discussion**

| # | Decision | Owner | Verdict | Rationale | Date |
|---|---|---|---|---|---|
| D1 | Endless node diminishing returns — Option A (cost-only scaling, no program change) | Jacob + design | _pending_ | | |
| D2 | Endless node diminishing returns — Option C (program change: `level_penalty_bps` field) | Jacob | _pending_ | | |
| D3 | If Option C: when to schedule? (v1.5 balance pass? post-launch? block Monday?) | Jacob + Joseph | _pending_ | | |

### Change log

- _2026-07-09 — Handoff doc created (Kingler). All 3 decisions marked `pending`._

---

## 7. What's already done (safe regardless of option)

- **Converter schema work** — `max_level` + `cost_growth_bps` fields added to `ResearchNodeSoTEntry` type and `emitResearchNodes` in `tools/c4-converter/src/{sot.ts, stages/phase4.ts}`. Conditional emit preserves byte-identical output for single-activation nodes. Regression tests pass. (Uncommitted on master as of 2026-07-09 — needs commit + PR.)
- **On-chain struct** — `ResearchNode.max_level` and `cost_growth_bps` already exist in `programs/sage/src/state/research.rs:171-173`. No program work needed to enable endless nodes at the struct level.
- **Redesign proposal** — `MINING-BUILDING-TREE-REDESIGN-PROPOSAL.md` (344 lines) covers full Mining/Building restructure including the 4 endless nodes. Awaiting Joseph's scope call on B-minimal vs B-full.
- **Verified CVC combine semantics** — `combine_repeated` path confirmed in source. Multiplicative vs additive vs max() rules mapped per field.

## 8. What's paused (blocked on this decision)

- **SoT data population** for the 4 endless node payloads — can't write `rare_mineral_discovery` maps or `max_productive_plots` values until we know whether the effect tapers
- **6 dead-node removals** (#83, #117, #124, #125, #126, #87) — independent of this decision, can ship separately
- **Faction split** (Building career #132/133/134) — independent, can ship separately
- **Construction Conditionals wiring** — independent, can ship separately

## 9. Data gaps

| Gap | Why it matters | Where to find it |
|---|---|---|
| Does `combine_repeated` need to handle `CharacterModifier::clone()`? | Option C requires cloning the modifier before scaling. `CharacterModifier` is `unsized_type` — may need a sized helper or different scaling approach. | Jacob / `programs/sage/src/state/research.rs:132` |
| Account migration path for `ResearchNode` if we add `level_penalty_bps` | Need to know if there's an existing realloc pattern or if this needs a new migration instruction | Jacob / existing admin instructions |
| Is `cost_growth_bps`'s linear (non-compounding) formula intentional? | If players expect exponential cost curves (EVE-style), the current linear scaling may feel too gentle at high levels. Separate from the effect-tapering question but related. | Design / bunthius |

---

## 10. Source references

### Primary program sources (verified line numbers)

- `programs/sage/src/state/research.rs:165-179` — `ResearchNode` struct with `max_level` + `cost_growth_bps` fields
- `programs/sage/src/state/research.rs:208-230` — `is_unlimited()`, `next_level()` (max_level=0 = endless)
- `programs/sage/src/state/research.rs:232-249` — `scaled_cost()` (linear cost growth formula)
- `programs/sage/src/state/research.rs:92-137` — `combine()` + `combine_repeated()` (CVC stacking rules)
- `programs/sage/src/state/research.rs:115-122` — `rare_mineral_discovery` multiplicative combine (`*existing *= *amount`)
- `programs/sage/src/state/research.rs:12-36` — `CharacterModifier` struct (full field list)

### Converter pipeline

- `sage-editor/tools/c4-converter/src/sot.ts:609-653` — `ResearchNodeSoTEntry` type with `max_level?` + `cost_growth_bps?`
- `sage-editor/tools/c4-converter/src/stages/phase4.ts:35-162` — `emitResearchNodes` with conditional field emit
- `sage-editor/tools/c4-converter/tests/regression.ts` — 5/5 built sections byte-equivalent

### Design artifacts

- `sage-editor/SAGE Editor Suite/Research Nodes/MINING-BUILDING-TREE-REDESIGN-PROPOSAL.md` — 344-line redesign proposal with full endless node specs
- `sage-editor/SAGE Editor Suite/Research Nodes/research_nodes-careercombatspread.json` — SoT data file (225 nodes, 11 with `scalability: "Unlimited"`, 0 with numeric `max_level`)

---

<div class="footer">
  <p><b>Endless Research Nodes — Program-Side Handoff</b> · 2026-07-09 · Kingler for Joseph Floyd</p>
  <p>Verified against <code>programs @ main</code> and <code>sage-editor @ master (d21010b)</code>.</p>
</div>
