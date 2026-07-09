# kingler-audit-docs

Hosting space for AI-assisted audit and decision documents (Star Atlas, MGK, etc.).
GitHub Pages serves the HTML; the markdown source lives alongside for diffing/review.

## Current docs

### C4 Cold-Start Audit & Decision Doc (2026-07-07)

Star Atlas · C4 progression — what a fresh character can actually do in each of the 6 careers, how long it takes to unlock the first Freelance node, and the open design questions that need sign-off.

- **Rendered:** https://kingler959.github.io/kingler-audit-docs/
- **Markdown source:** [c4-cold-start-decision-doc.md](./c4-cold-start-decision-doc.md)

**Open decisions in this doc (D1-D6):**
1. Scan XP formula (`base × scan_power`) — intended?
2. Combat cold-start survivability — weapon module? training NPC?
3. Building XP ceiling — what is `building_def.xp_value`?
4. Scan cooldown pacing (786s → 60-90s?)
5. Bundle additions — confirm Cult Claims + Stims mints/IDs
6. Ship-size communication in UI

Each is scoped to be answerable with Accept / Change / Defer.

### Endless Research Nodes — Program-Side Handoff (2026-07-09)

Star Atlas · C4 progression — program-team handoff on diminishing-returns curves for endless prestige research nodes. Three options ranging from "ship as-is" to "program change + account migration," with worked examples and source-verified mechanics.

- **Rendered:** https://kingler959.github.io/kingler-audit-docs/endless-nodes-program-handoff.html
- **Markdown source:** [endless-nodes-program-handoff.md](./endless-nodes-program-handoff.md)

**Open decisions in this doc (D1-D3):**
1. Option A — Ship as-is with linear cost scaling (no program change)
2. Option C — Program change: add `level_penalty_bps` field to `ResearchNode`
3. If Option C: when to schedule? (block Monday / v1.5 / post-launch)

Each is scoped to be answerable with Accept / Change / Defer.
