"""Mutation check for Day 2: do your tests actually catch bugs?

Runs tests/test_taikun.py once against the correct fake API, then once per
planted bug. A good suite passes on the correct version and FAILS on every
mutant ("caught"). A mutant your suite still passes on has "survived".

    uv run python tools/check_mutants.py
"""

import os
import subprocess
import sys

MUTANTS = {
    "no_name_validation": "accepts any cluster name",
    "nodes_upper_bound": "accepts 101 nodes",
    "duplicate_allowed": "creating an existing name silently overwrites it",
    "quota_off_by_one": "allows one cluster more than the quota",
    "leaky_quota": "deleting a cluster doesn't free its quota",
    "delete_silent": "deleting an unknown cluster doesn't raise",
    "never_ready": "clusters stay PENDING forever",
    "upgrade_skips_check": "allows any upgrade, e.g. skipping minor versions",
}

TEST_FILE = "tests/test_taikun.py"


def run(mutant: str | None) -> bool:
    """Return True if the test suite passed."""
    env = {k: v for k, v in os.environ.items() if k != "TAIKUN_MUTANT"}
    if mutant:
        env["TAIKUN_MUTANT"] = mutant
    cmd = [sys.executable, "-m", "pytest", TEST_FILE, "-q", "-x", "-p", "no:cacheprovider"]
    result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=300)
    return result.returncode == 0


def main() -> int:
    print("Baseline (correct API) ...", end=" ", flush=True)
    if not run(None):
        print("FAILED")
        print(f"Your tests must pass on the correct API first: uv run pytest {TEST_FILE} -v")
        return 1
    print("passed\n")

    survived = []
    for name, description in MUTANTS.items():
        caught = not run(name)
        print(f"  {'caught  ' if caught else 'SURVIVED'}  {name:<22} {description}")
        if not caught:
            survived.append(name)

    total = len(MUTANTS)
    print(f"\n{total - len(survived)}/{total} bugs caught.")
    if survived:
        print("Write a test that would fail for each SURVIVED bug, then run this again.")
    return 1 if survived else 0


if __name__ == "__main__":
    sys.exit(main())
