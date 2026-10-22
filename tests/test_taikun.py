"""Day 2: you write the tests.

System under test: src/python_refresh/taikun_fake.py (read its docstring first).
Fixtures: tests/conftest.py (TODO 1-4 live there).

    uv run pytest tests/test_taikun.py -v           # your tests must pass
    uv run python tools/check_mutants.py            # ...and catch all 8 planted bugs

Replace each TODO with one or more test functions.
"""

import pytest

from python_refresh.cluster import wait_until
from python_refresh.taikun_fake import (
    ClusterNotFoundError,
    ClusterNotReadyError,
    DuplicateClusterError,
    QuotaExceededError,
    UpgradeNotAllowedError,
    ValidationError,
)

# ---------------------------------------------------------------------------
# Part A: using fixtures
# ---------------------------------------------------------------------------
# TODO 5 — A new cluster (use the `cluster` fixture) is PENDING, with the
#          default version "1.30.0" and 1 node.

# TODO 6 — The cluster becomes RUNNING. Poll with your wait_until() and a short
#          timeout and interval (e.g. timeout=1, interval=0.01), never time.sleep.
#          Mark this test @pytest.mark.slow (see TODO 16).

# ---------------------------------------------------------------------------
# Part B: parametrize
# ---------------------------------------------------------------------------
# TODO 7 — Valid names are accepted. One parametrized test, at least 4 names,
#          including edge cases (shortest and longest allowed). Give the cases
#          readable ids with `ids=[...]` or pytest.param(..., id="...").

# TODO 8 — Invalid names raise ValidationError. At least 5 cases. Use
#          pytest.raises(ValidationError, match="Invalid cluster name").

# TODO 9 — Node count boundaries: 0, 1, 100 and 101 in ONE parametrized test.
#          Hint: parametrize the expected outcome too, e.g. (nodes, should_pass).

# ---------------------------------------------------------------------------
# Part C: business rules (use `client` and `make_cluster`)
# ---------------------------------------------------------------------------
# TODO 10 — Creating a cluster with an existing name raises DuplicateClusterError.

# TODO 11 — Quota: with quota=3, the 4th cluster raises QuotaExceededError.

# TODO 12 — Deleting a cluster frees its quota slot.

# TODO 13 — Deleting a cluster that doesn't exist raises ClusterNotFoundError.

# TODO 14 — Upgrade rules, parametrized: from a RUNNING 1.30.0 cluster, check
#           allowed targets (patch up, one minor up) and blocked ones (skip a
#           minor, downgrade, same version, new major).

# TODO 15 — Upgrading a cluster that is still PENDING raises ClusterNotReadyError.

# ---------------------------------------------------------------------------
# Part D: markers and running (no code in this file)
# ---------------------------------------------------------------------------
# TODO 16 — Register `slow` and `smoke` markers in pyproject.toml under
#           [tool.pytest.ini_options] (your --strict-markers setting makes
#           unregistered markers an error). Mark 2-3 core fast tests as smoke, then
#           try:  uv run pytest -m smoke   and   uv run pytest -m "not slow"

# TODO 17 — uv add --dev pytest-xdist, then:  uv run pytest -n auto
#           Your fixtures must be isolated for this to stay green.
