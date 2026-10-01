#!/usr/bin/env python3
"""Reproduce Targeting old-layout behavior at pinned Programs commits.

This is a compatibility characterization package, not a runtime safety fix and
not a fresh-genesis fixture generator. It extracts old Game bytes directly from
the pinned base Git object, runs actual base/head Rust decoders, then runs the
checked-in generated TypeScript decoder at the pinned head.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE = "9676a9f0a16186443fa86d141d3112762dc704cd"
HEAD = "4ee78371521df9ecfe0fae926f5f4201881d07a6"
FIXTURE_PATH = "fixtures/game-genesis.bin"
SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = SCRIPT_DIR / "templates"
EXPECTATIONS_PATH = SCRIPT_DIR / "expected-old-layout.json"
WORK_DIR_MARKER = ".targeting-old-layout-proof-workdir-v1"


class ProofError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def run(
    command: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    binary: bool = False,
) -> str | bytes:
    print(f"$ (cd {cwd} && {' '.join(command)})", flush=True)
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=not binary,
        check=False,
    )
    if binary:
        output = completed.stdout
    else:
        output = completed.stdout or ""
        print(output, end="" if output.endswith("\n") else "\n", flush=True)
    if completed.returncode != 0:
        raise ProofError(f"command failed with exit {completed.returncode}: {' '.join(command)}")
    return output


def git_text(worktree: Path, *args: str) -> str:
    return str(run(["git", *args], cwd=worktree)).strip()


def paths_overlap(left: Path, right: Path) -> bool:
    return left == right or left.is_relative_to(right) or right.is_relative_to(left)


def require_disjoint_path(candidate: Path, protected: list[Path], label: str) -> None:
    for root in protected:
        if paths_overlap(candidate, root):
            raise ProofError(f"{label} {candidate} overlaps protected path {root}")


def require_exact_clean_worktree(worktree: Path, expected_head: str) -> None:
    actual_head = git_text(worktree, "rev-parse", "HEAD")
    if actual_head != expected_head:
        raise ProofError(f"{worktree}: expected HEAD {expected_head}, got {actual_head}")
    status = git_text(worktree, "status", "--porcelain")
    if status:
        raise ProofError(f"{worktree}: worktree is not clean before proof:\n{status}")
    remote = git_text(worktree, "remote", "get-url", "origin")
    if remote.rstrip("/").removesuffix(".git") != "https://github.com/staratlasmeta/programs":
        raise ProofError(f"{worktree}: unexpected origin {remote}")
    symbolic = subprocess.run(
        ["git", "symbolic-ref", "-q", "HEAD"],
        cwd=worktree,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    if symbolic.returncode == 0:
        raise ProofError(
            f"{worktree}: expected detached HEAD, found {symbolic.stdout.strip() or 'symbolic HEAD'}"
        )
    if symbolic.returncode != 1:
        raise ProofError(
            f"{worktree}: unable to verify detached HEAD (exit {symbolic.returncode}): "
            f"{symbolic.stdout.strip()}"
        )


def prepare_work_dir(work_dir: Path) -> None:
    if work_dir.exists():
        if work_dir.is_symlink() or not work_dir.is_dir():
            raise ProofError(f"--work-dir must be a real directory, not a symlink/file: {work_dir}")
        marker = work_dir / WORK_DIR_MARKER
        if (
            marker.is_symlink()
            or not marker.is_file()
            or marker.read_text() != "targeting-old-layout-proof/v1\n"
        ):
            raise ProofError(
                f"refusing to remove unmarked existing --work-dir {work_dir}; "
                f"expected exact regular marker {marker}"
            )
        shutil.rmtree(work_dir)
    work_dir.mkdir(parents=True)
    (work_dir / WORK_DIR_MARKER).write_text("targeting-old-layout-proof/v1\n")


def stage_atomic_result(result_path: Path, content: str) -> Path:
    result_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{result_path.name}.", suffix=".tmp", dir=result_path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise
    return temporary_path


def commit_atomic_result(temporary_path: Path, result_path: Path) -> None:
    os.replace(temporary_path, result_path)
    directory_fd = os.open(result_path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def parse_marker(output: str, name: str) -> str:
    match = re.search(rf"^{re.escape(name)}=(.*)$", output, flags=re.MULTILINE)
    if not match:
        raise ProofError(f"missing marker {name}")
    return match.group(1).strip()


def parse_kv_marker(value: str) -> dict[str, int | str]:
    parsed: dict[str, int | str] = {}
    for item in value.split(","):
        key, raw = item.split(":", 1)
        parsed[key] = int(raw) if raw.isdigit() else raw
    return parsed


def witness_metadata(path: Path) -> dict[str, Any]:
    return {"size": path.stat().st_size, "sha256": sha256_file(path)}


def verify_expected(label: str, actual: Any, expected: Any) -> None:
    if actual != expected:
        raise ProofError(f"{label}: expected {expected!r}, got {actual!r}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-worktree", type=Path, required=True)
    parser.add_argument("--head-worktree", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--base-target-dir", type=Path, required=True)
    parser.add_argument("--head-target-dir", type=Path, required=True)
    args = parser.parse_args()

    base_worktree = args.base_worktree.resolve()
    head_worktree = args.head_worktree.resolve()
    work_dir = args.work_dir.resolve()
    result_path = args.result.resolve()
    base_target_dir = args.base_target_dir.resolve()
    head_target_dir = args.head_target_dir.resolve()
    expectations = json.loads(EXPECTATIONS_PATH.read_text())

    temp_root = Path("/tmp").resolve()
    if work_dir == temp_root or not work_dir.is_relative_to(temp_root):
        raise ProofError(
            f"--work-dir must be a dedicated child of {temp_root}; refusing destructive cleanup of {work_dir}"
        )
    if not work_dir.name.startswith("targeting-old-layout-proof"):
        raise ProofError(
            "--work-dir basename must start with 'targeting-old-layout-proof' to mark its purpose"
        )
    protected_worktrees = [base_worktree, head_worktree]
    require_disjoint_path(work_dir, protected_worktrees, "--work-dir")
    require_disjoint_path(result_path, protected_worktrees, "--result")
    require_disjoint_path(result_path, [work_dir], "--result")
    if result_path.exists() and result_path.is_dir():
        raise ProofError(f"--result must be a file path, not a directory: {result_path}")
    if paths_overlap(base_target_dir, head_target_dir):
        raise ProofError("--base-target-dir and --head-target-dir must be disjoint")
    require_disjoint_path(
        base_target_dir,
        [*protected_worktrees, work_dir, result_path],
        "--base-target-dir",
    )
    require_disjoint_path(
        head_target_dir,
        [*protected_worktrees, work_dir, result_path],
        "--head-target-dir",
    )

    verify_expected("expectation base commit", expectations["base_commit"], BASE)
    verify_expected("expectation head commit", expectations["head_commit"], HEAD)
    require_exact_clean_worktree(base_worktree, BASE)
    require_exact_clean_worktree(head_worktree, HEAD)

    base_test = base_worktree / "programs/sage/tests/targeting_old_byte_base_probe.rs"
    head_test = head_worktree / "programs/sage/tests/targeting_old_byte_head_probe.rs"
    ts_test = head_worktree / "clients/packages/sage/tests/targeting-old-byte-proof.test.ts"
    temporary_files = [base_test, head_test, ts_test]
    for path in temporary_files:
        if path.exists():
            raise ProofError(f"refusing to overwrite existing temporary proof file: {path}")

    prepare_work_dir(work_dir)
    fixture_file = work_dir / "game-genesis.base.bin"

    blob_oid = git_text(base_worktree, "rev-parse", f"{BASE}:{FIXTURE_PATH}")
    fixture_bytes = run(
        ["git", "show", f"{BASE}:{FIXTURE_PATH}"],
        cwd=base_worktree,
        binary=True,
    )
    assert isinstance(fixture_bytes, bytes)
    fixture_file.write_bytes(fixture_bytes)
    fixture = {
        "path": FIXTURE_PATH,
        "git_blob_oid": blob_oid,
        "sha256": sha256_bytes(fixture_bytes),
        "size": len(fixture_bytes),
        "discriminator_hex": fixture_bytes[:8].hex(),
    }
    for key, expected in expectations["fixture"].items():
        verify_expected(f"fixture {key}", fixture[key], expected)

    commands: list[dict[str, Any]] = []
    try:
        shutil.copyfile(TEMPLATE_DIR / "base_probe.rs", base_test)
        shutil.copyfile(TEMPLATE_DIR / "head_probe.rs", head_test)
        shutil.copyfile(TEMPLATE_DIR / "head_ts_probe.test.ts", ts_test)

        base_env = os.environ.copy()
        base_env.update(
            {
                "CARGO_TARGET_DIR": str(base_target_dir),
                "TARGETING_OLD_GAME_FIXTURE": str(fixture_file),
                "TARGETING_PROOF_OUTPUT_DIR": str(work_dir),
            }
        )
        base_command = [
            "cargo",
            "test",
            "-p",
            "sage_star_frame",
            "--test",
            "targeting_old_byte_base_probe",
            "--",
            "--nocapture",
        ]
        base_output = str(run(base_command, cwd=base_worktree, env=base_env))
        commands.append({"cwd": str(base_worktree), "command": base_command, "result": "PASS"})

        base_count = int(parse_marker(base_output, "TARGETING_PROOF_BASE_NODE_COUNT"))
        base_ids = [
            int(value)
            for value in parse_marker(base_output, "TARGETING_PROOF_BASE_NODE_IDS").split(",")
            if value
        ]
        base_layout = parse_kv_marker(parse_marker(base_output, "TARGETING_PROOF_BASE_LAYOUT"))
        base_alignments = parse_kv_marker(
            parse_marker(base_output, "TARGETING_PROOF_BASE_ALIGNMENTS")
        )
        verify_expected(
            "base node count", base_count, expectations["base_decoder"]["expected_node_count"]
        )
        verify_expected(
            "base node IDs", base_ids, expectations["base_decoder"]["expected_node_ids"]
        )
        verify_expected("base layout", base_layout, expectations["base_layout"])
        verify_expected("base alignments", base_alignments, expectations["base_alignments"])

        old_value_witnesses: dict[str, Any] = {}
        for name, expected in expectations["old_value_witnesses"].items():
            metadata = witness_metadata(work_dir / name)
            verify_expected(f"{name} size", metadata["size"], expected["size"])
            verify_expected(f"{name} sha256", metadata["sha256"], expected["sha256"])
            old_value_witnesses[name] = metadata

        head_env = os.environ.copy()
        head_env.update(
            {
                "CARGO_TARGET_DIR": str(head_target_dir),
                "TARGETING_OLD_GAME_FIXTURE": str(fixture_file),
                "TARGETING_PROOF_OUTPUT_DIR": str(work_dir),
                "TARGETING_EXPECTED_BASE_NODE_COUNT": str(base_count),
            }
        )
        head_command = [
            "cargo",
            "test",
            "-p",
            "sage_star_frame",
            "--test",
            "targeting_old_byte_head_probe",
            "--",
            "--nocapture",
        ]
        head_output = str(run(head_command, cwd=head_worktree, env=head_env))
        commands.append({"cwd": str(head_worktree), "command": head_command, "result": "PASS"})
        head_results = parse_kv_marker(
            parse_marker(head_output, "TARGETING_PROOF_HEAD_RESULTS")
        )
        head_layout = parse_kv_marker(parse_marker(head_output, "TARGETING_PROOF_HEAD_LAYOUT"))
        head_alignments = parse_kv_marker(
            parse_marker(head_output, "TARGETING_PROOF_HEAD_ALIGNMENTS")
        )

        expected_head_results = expectations["known_unsupported_head_results"]
        verify_expected(
            "head CharacterModifier result",
            head_results["character_modifier"],
            expected_head_results["rust_character_modifier"],
        )
        verify_expected(
            "head Character result",
            head_results["character"],
            expected_head_results["rust_character"],
        )
        verify_expected(
            "head CharacterSync result",
            head_results["character_sync"],
            expected_head_results["rust_character_sync"],
        )
        verify_expected(
            "head ResearchTree result",
            head_results["research_tree_one_node"],
            expected_head_results["rust_research_tree_one_node"],
        )
        verify_expected(
            "head Game result",
            head_results[f"game_{base_count}_nodes"],
            expected_head_results["rust_game_63_nodes"],
        )
        verify_expected("head layout", head_layout, expectations["head_layout"])
        verify_expected("head alignments", head_alignments, expectations["head_alignments"])

        vitest = head_worktree / "clients/node_modules/.bin/vitest"
        if not vitest.exists():
            raise ProofError(
                "exact-head clients/node_modules is missing; run the README's frozen-lockfile install"
            )
        ts_env = os.environ.copy()
        ts_env["TARGETING_OLD_GAME_FIXTURE"] = str(fixture_file)
        ts_result_path = work_dir / "head-generated-typescript-result.json"
        ts_env["TARGETING_TS_RESULT"] = str(ts_result_path)
        ts_command = [
            "pnpm",
            "--filter",
            "@staratlas/dev-sage",
            "exec",
            "vitest",
            "--run",
            "tests/targeting-old-byte-proof.test.ts",
        ]
        run(ts_command, cwd=head_worktree / "clients", env=ts_env)
        commands.append(
            {"cwd": str(head_worktree / "clients"), "command": ts_command, "result": "PASS"}
        )
        if not ts_result_path.exists():
            raise ProofError("generated TypeScript probe did not write its result file")
        ts_result = json.loads(ts_result_path.read_text())
        verify_expected("TypeScript decoder status", ts_result["status"], "error")
        if not re.search(r"Codec \[u16\] expected 2 bytes, got 1", ts_result["message"]):
            raise ProofError(f"unexpected TypeScript decoder error: {ts_result['message']}")

        result = {
            "schema": "targeting-old-layout-proof-result/v1",
            "captured_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "classification": "KNOWN_UNSUPPORTED_OLD_LAYOUT_CHARACTERIZATION",
            "safety_claim": False,
            "fresh_fixture_claim": False,
            "base_commit": BASE,
            "head_commit": HEAD,
            "fixture": fixture,
            "expected_manifest_sha256": sha256_file(EXPECTATIONS_PATH),
            "template_sha256": {
                path.name: sha256_file(path)
                for path in sorted(TEMPLATE_DIR.iterdir())
                if path.is_file()
            },
            "base_decoder": {
                "node_count": base_count,
                "node_ids": base_ids,
                "layout": base_layout,
                "alignments": base_alignments,
            },
            "old_value_witnesses": old_value_witnesses,
            "head_rust_decoder": {
                "results": head_results,
                "layout": head_layout,
                "alignments": head_alignments,
            },
            "head_generated_typescript_decoder": ts_result,
            "commands": commands,
            "owner_decision_required": [
                "ACCEPT_FRESH_ONLY_EXCLUSION_AND_CORRECTED_DOCS_QUALIFICATION_GUARD",
                "REQUEST_SEPARATE_RUNTIME_OLD_LAYOUT_REFUSAL_DESIGN",
            ],
        }
    finally:
        for path in temporary_files:
            path.unlink(missing_ok=True)

    require_exact_clean_worktree(base_worktree, BASE)
    require_exact_clean_worktree(head_worktree, HEAD)
    result["completion"] = {
        "overall_result": "PASS",
        "temporary_probes_removed": True,
        "base_worktree_clean_and_detached_after_probe_cleanup": True,
        "head_worktree_clean_and_detached_after_probe_cleanup": True,
        "result_path_outside_programs_worktrees": True,
        "result_write_mode": "atomic_temp_fsync_replace",
    }
    temporary_result = stage_atomic_result(
        result_path, json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    try:
        # Writing the staged result must not perturb either protected worktree. Check once more
        # immediately before the atomic replacement that makes the result visible.
        require_exact_clean_worktree(base_worktree, BASE)
        require_exact_clean_worktree(head_worktree, HEAD)
        commit_atomic_result(temporary_result, result_path)
    finally:
        temporary_result.unlink(missing_ok=True)
    print(f"atomically wrote verified result after cleanup and final checks: {result_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ProofError as error:
        print(f"PROOF FAILED: {error}", file=sys.stderr)
        raise SystemExit(1)
