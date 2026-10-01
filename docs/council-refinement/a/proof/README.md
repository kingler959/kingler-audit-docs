# Targeting old-layout compatibility proof

This package makes Lane A's temporary layout probes durable and reproducible without modifying the Programs producer branch.

It is a **known unsupported-old-layout characterization**, not a runtime safety fix, migration, fresh-genesis fixture, or release gate. A successful run proves that the pinned decoders still exhibit the recorded incompatible outcomes; it does not make those outcomes safe.

## Pinned inputs

- Programs base: `9676a9f0a16186443fa86d141d3112762dc704cd`
- Programs #1042 head: `4ee78371521df9ecfe0fae926f5f4201881d07a6`
- Old Game source: `fixtures/game-genesis.bin` read with `git show` from the exact base object
- Old Game blob: `2f677ca8438da025f826d76ee99f9afc00aabaaf`
- Old Game SHA-256: `2cdd667413456bd117d99e6860260041a87634bcfbe90cc259c1f4ce18e7a141`
- Game discriminator: `1b5aa67d4a647912`
- Expected base node set: 63 exact IDs in [`expected-old-layout.json`](expected-old-layout.json)

The raw Game and temporary Character/CharacterSync/ResearchTree witnesses are generated into the caller's work directory. They are not copied into this repository.

## What executes

1. Verify clean detached base/head worktrees and exact remote/commit identities.
2. Recover the old Game bytes directly from the base Git object and verify blob, byte SHA-256, size, and discriminator.
3. Compile and run the base Rust decoder to:
   - prove all 63 expected node IDs;
   - serialize default old-layout CharacterModifier, Character, CharacterSync, and one-node ResearchTree values;
   - verify their pinned byte sizes, alignments, offsets and SHA-256 identities.
4. Compile and run the head Rust decoder to record the known unsupported outcomes:
   - old CharacterModifier, Character, and CharacterSync reject with `RawSliceAdvance`;
   - old one-node ResearchTree is accepted as zero nodes;
   - old 63-node Game is accepted as zero nodes;
   - new fixed/default layout sizes and field offsets remain pinned.
5. Run the actual checked-in generated TypeScript Game decoder at the exact head. It rejects the old Game bytes with `Codec [u16] expected 2 bytes, got 1`.
6. Remove every temporary probe from both Programs worktrees and require both worktrees to be clean again.
7. Only after cleanup and both clean/detached-worktree checks pass, stage the result outside both Programs worktrees, recheck both worktrees, then publish the result with a temp-file + `fsync` + atomic replacement.

No source-string assertions are used for decoder behavior.

## Prerequisite: exact-head client install

The TypeScript proof deliberately uses the exact worktree's dependency graph. Do not symlink another checkout's `node_modules`.

```bash
cd /root/staratlas/programs-worktrees/targeting-schema-4ee78371/clients
CI=true pnpm install --frozen-lockfile --prefer-offline
pnpm --filter @staratlas/dev-player-profile build
pnpm --filter @staratlas/dev-profile-faction build
```

The two dependency builds are required before Vitest imports the SAGE generated graph; an install alone leaves their declared `dist` exports absent.

## Run

```bash
python3 docs/council-refinement/a/proof/run.py \
  --base-worktree /root/staratlas/programs-worktrees/targeting-base-9676 \
  --head-worktree /root/staratlas/programs-worktrees/targeting-schema-4ee78371 \
  --work-dir /tmp/targeting-old-layout-proof-v1 \
  --base-target-dir /root/staratlas/targets/targeting-base-layout \
  --head-target-dir /root/staratlas/targets/targeting-head-layout \
  --result docs/council-refinement/a/proof/results/verified-run.json
```

The committed result is a parsed evidence record. Compiler logs and generated old bytes stay outside Git.

The work directory must be a non-overlapping `/tmp/targeting-old-layout-proof*` directory. Once created, the runner writes a purpose marker and refuses to recursively clean any pre-existing directory without that exact regular marker. The result path must be outside the work directory and both protected Programs worktrees.

## Interpretation

The proof's overall command exits zero only when the **known unsupported** behavior matches the pinned manifest. That is intentionally different from claiming an old target is safe:

- Rust's old Game acceptance with 63 → 0 research nodes remains a release blocker.
- TypeScript rejection does not compensate for the Rust runtime's semantic truncation.
- D still owns fresh selected universe/genesis/fixture generation and expected-node equality on those new bytes.
- C must refuse the published old SDK/target combination.

## Producer decision

The original producer must choose one of two explicit paths:

1. **Accept fresh-only exclusion** — correct the documentation, retain the existing deployed-game exclusion, and require D's exact fresh-genesis node-equality/decoder qualification guard.
2. **Request a separate old-layout refusal design** — scope and review an explicit runtime guard as a new Programs change. This proof does not invent an account version or migration.

The author-ready source proposal is [`producer-correction.patch`](producer-correction.patch). It is intentionally emitted as a zero-context patch so the audit repository can retain it without whitespace-only context lines; verify/apply it at exact Programs `4ee783715…` with `git apply --unidiff-zero --check` / `git apply --unidiff-zero`. It is not applied to Programs without an explicit handoff.
