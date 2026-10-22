"""Tests for Day 1. Don't edit these — make them pass by changing cluster.py."""

import dataclasses
import time

import pytest

from python_refresh import cluster as c


# --- 1. Exceptions ---------------------------------------------------------
def test_custom_exceptions_share_a_base_class():
    assert issubclass(c.DuplicatePoolError, c.ClusterError)
    assert issubclass(c.InvalidVersionError, c.ClusterError)


# --- 2. Dataclasses --------------------------------------------------------
def test_node_pool_defaults_and_equality():
    pool = c.NodePool("workers", 3)
    assert pool.machine_type == "standard"
    assert pool == c.NodePool("workers", 3, "standard")  # dataclasses give you __eq__


def test_node_pool_is_immutable():
    pool = c.NodePool("workers", 3)
    with pytest.raises(dataclasses.FrozenInstanceError):
        pool.size = 5


def test_node_pool_rejects_empty_size():
    with pytest.raises(ValueError):
        c.NodePool("workers", 0)


def test_cluster_total_nodes():
    cl = c.Cluster("prod", "1.29.3")
    cl.add_pool(c.NodePool("system", 2))
    cl.add_pool(c.NodePool("workers", 5, "gpu"))
    assert cl.total_nodes == 7


def test_cluster_rejects_duplicate_pool():
    cl = c.Cluster("prod", "1.29.3")
    cl.add_pool(c.NodePool("workers", 3))
    with pytest.raises(c.DuplicatePoolError):
        cl.add_pool(c.NodePool("workers", 1))


def test_clusters_do_not_share_pool_lists():
    a = c.Cluster("a", "1.29.0")
    b = c.Cluster("b", "1.29.0")
    a.add_pool(c.NodePool("workers", 1))
    assert b.node_pools == []


# --- 3. Parsing ------------------------------------------------------------
@pytest.mark.parametrize(
    "raw, expected",
    [("1.29.3", (1, 29, 3)), ("v1.30.0", (1, 30, 0)), ("2.0.10", (2, 0, 10))],
)
def test_parse_version_valid(raw, expected):
    assert c.parse_version(raw) == expected


@pytest.mark.parametrize("raw", ["1.29", "abc", "1.x.3", "", "1.29.3.4"])
def test_parse_version_invalid(raw):
    with pytest.raises(c.InvalidVersionError):
        c.parse_version(raw)


@pytest.mark.parametrize(
    "current, target, allowed",
    [
        ("1.29.3", "1.30.0", True),  # one minor up
        ("1.29.3", "1.29.5", True),  # patch up
        ("1.29.3", "1.31.0", False),  # skips a minor
        ("1.29.3", "1.28.9", False),  # downgrade
        ("1.29.3", "1.29.3", False),  # same version
        ("1.29.3", "2.0.0", False),  # major change
    ],
)
def test_can_upgrade(current, target, allowed):
    assert c.can_upgrade(current, target) is allowed


# --- 4. Context managers ---------------------------------------------------
class FakeClient:
    def __init__(self):
        self.created, self.deleted = [], []

    def create_cluster(self, name):
        self.created.append(name)
        return c.Cluster(name, "1.29.0")

    def delete_cluster(self, name):
        self.deleted.append(name)


def test_temporary_cluster_yields_and_cleans_up():
    client = FakeClient()
    with c.temporary_cluster(client, "e2e-1") as cl:
        assert cl.name == "e2e-1"
        assert client.deleted == []  # not deleted while still in use
    assert client.deleted == ["e2e-1"]


def test_temporary_cluster_cleans_up_even_on_failure():
    client = FakeClient()
    with pytest.raises(RuntimeError):
        with c.temporary_cluster(client, "e2e-2"):
            raise RuntimeError("test blew up")
    assert client.deleted == ["e2e-2"]


# --- 5. Polling ------------------------------------------------------------
def test_wait_until_returns_first_truthy_value():
    calls = iter([None, "", "READY"])
    assert c.wait_until(lambda: next(calls), timeout=2, interval=0.01) == "READY"


def test_wait_until_times_out():
    start = time.monotonic()
    with pytest.raises(TimeoutError):
        c.wait_until(lambda: False, timeout=0.2, interval=0.05)
    assert time.monotonic() - start < 1  # gave up promptly


# --- 6. Comprehensions -----------------------------------------------------
def test_unhealthy_pods():
    pods = [
        {"name": "api-1", "status": "Running", "ready": True},
        {"name": "api-2", "status": "Running", "ready": False},
        {"name": "db-0", "status": "CrashLoopBackOff", "ready": False},
        {"name": "job-x", "status": "Running"},  # no "ready" key
        {"name": "web-1", "status": "Running", "ready": True},
    ]
    assert c.unhealthy_pods(pods) == ["api-2", "db-0", "job-x"]
