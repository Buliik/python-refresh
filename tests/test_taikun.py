"""Day 2: you write the tests.

System under test: src/python_refresh/taikun_fake.py (read its docstring first).
Fixtures: tests/conftest.py (1-4 live there).

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
# 5 — A new cluster (use the `cluster` fixture) is PENDING, with the
#          default version "1.30.0" and 1 node.
def test_cluster_pending(cluster):
    assert cluster.status == "PENDING"
    assert cluster.k8s_version == "1.30.0"
    assert cluster.nodes == 1


# 6 — The cluster becomes RUNNING. Poll with your wait_until() and a short
#          timeout and interval (e.g. timeout=1, interval=0.01), never time.sleep.
#          Mark this test @pytest.mark.slow (see 16).
@pytest.mark.slow
def test_cluster_becomes_running(client, cluster):
    running = wait_until(
        lambda: client.get_cluster(cluster.name).status == "RUNNING", timeout=1, interval=0.01
    )
    assert running


# ---------------------------------------------------------------------------
# Part B: parametrize
# ---------------------------------------------------------------------------
# TODO 7 — Valid names are accepted. One parametrized test, at least 4 names,
#          including edge cases (shortest and longest allowed). Give the cases
#          readable ids with `ids=[...]` or pytest.param(..., id="...").


@pytest.mark.parametrize(
    "name",
    [
        pytest.param("a", id="shortest"),
        pytest.param("valid-name-with-dashes", id="normal"),
        pytest.param("a" * 40, id="longest"),
        pytest.param("1-name-starting-with-digit-123", id="with-digits"),
    ],
)
def test_valid_names(client, name):
    info = client.create_cluster(name=name)
    assert info.name == name


# 8 — Invalid names raise ValidationError. At least 5 cases. Use
#          pytest.raises(ValidationError, match="Invalid cluster name").


@pytest.mark.parametrize(
    "name",
    [
        pytest.param("", id="empty"),
        pytest.param("invalid_name_with_underscores", id="with-underscores"),
        pytest.param("invalid-name-ending-with-dash-", id="ending-dash"),
        pytest.param("-invalid-name-leading-with-dash", id="leading-dash"),
        pytest.param("Invalid-name-uppercase", id="with-uppercase"),
        pytest.param("a" * 41, id="too-long"),
    ],
)
def test_invalid_names(client, name):
    with pytest.raises(ValidationError, match="Invalid cluster name"):
        client.create_cluster(name=name)


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
