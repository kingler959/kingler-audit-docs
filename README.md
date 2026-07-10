# kingler-audit-docs

Hosting space for AI-assisted audit and decision documents (Star Atlas, MGK, etc.).
GitHub Pages serves the HTML; the markdown source lives alongside for diffing/review.

## Current docs

### C4 Cold-Start Audit & Decision Doc (2026-07-10)

Star Atlas · C4 progression contract — source-verified first-action availability for all six careers, generated-data/SoT gate divergence, starter recipe/material coverage, first-hours models, and explicit pre-regen decisions.

- **Rendered:** https://kingler959.github.io/kingler-audit-docs/
- **Markdown source:** [c4-cold-start-decision-doc.md](./c4-cold-start-decision-doc.md)
- **Executable audit:** [c4-cold-start-audit.py](./c4-cold-start-audit.py)

**Open decisions in this doc (D1-D6):**
1. Claim Stake T1 gate — immediate starter slot, six levels, or twelve levels?
2. Starter hub materials — tutorial-specific kit, universal kit, or mining dependency?
3. Combat bootstrap — starter typed damage + target, or explicit deferral?
4. Public Crafting progression — per-Character cap, XP budget, or accept fan-out?
5. Recipe SoT — block regen, use explicit live pass-through, or defer gates?
6. Onboarding UI contract — required before launch or follow-up?

The rendered page stores responses locally and exports Markdown or JSON.

### Endless Research Nodes — Program-Side Handoff (2026-07-09)

Star Atlas · C4 progression — program-team handoff on diminishing-returns curves for endless prestige research nodes. Three options ranging from "ship as-is" to "program change + account migration," with worked examples and source-verified mechanics.

- **Rendered:** https://kingler959.github.io/kingler-audit-docs/endless-nodes-program-handoff.html
- **Markdown source:** [endless-nodes-program-handoff.md](./endless-nodes-program-handoff.md)

**Open decisions in this doc (D1-D3):**
1. Option A — Ship as-is with linear cost scaling (no program change)
2. Option C — Program change: add `level_penalty_bps` field to `ResearchNode`
3. If Option C: when to schedule? (block Monday / v1.5 / post-launch)

Each is scoped to be answerable with Accept / Change / Defer.

### C4 Mining & Building Trees — Verified Structure + Proposed Changes (2026-07-09)

Star Atlas · C4 progression — verified current state of the Mining and Building research trees (correcting factual errors in the original redesign proposal), with individually-approve-able change proposals for dead-node removal, endless-node activation, and terrain-conditional wiring.

- **Rendered:** https://kingler959.github.io/kingler-audit-docs/c4-mining-building-verified-trees.html
- **Markdown source:** [c4-mining-building-verified-trees.md](./c4-mining-building-verified-trees.md)

**Open decisions in this doc (M1-M4, B1-B6):**
- M1: Remove 5 dead Mining nodes (#83, #117, #124, #125, #126)
- M2: Activate #82 Rare Minerals as endless
- M3: Add #377 Deep Vein Extraction (new endless)
- M4: Vapor Beam coverage (expand/leave/merge)
- B1: Assign #379 to Construction Conditionals, flip v2→v1
- B2: Flip 4 terrain conditionals to v1 (#380-#383)
- B3: Move #135 Medium Risk under Construction Conditionals
- B4: Remove #87 Regional Construction Tiers (hollow spine)
- B5: Add #378 Industrial Throughput (new endless)
- B6: Building slot endless #384? (add/defer/skip)

Each is scoped to be answerable with Approve / Reject / Modify / Needs discussion.
