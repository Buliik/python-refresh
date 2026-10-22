"""Day 1 — Python refresh.

Implement everything marked TODO, then run:

    uv run pytest tests/test_cluster.py -v

Work top to bottom; each section maps to one group of tests.
Requires Python 3.10+ (your project uses 3.13).
"""

from __future__ import annotations

import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Protocol, TypeVar

T = TypeVar("T")


# ---------------------------------------------------------------------------
# 1. Exceptions
# ---------------------------------------------------------------------------
class ClusterError(Exception):
    """Base class for every error raised by this module (given)."""


class DuplicatePoolError(ClusterError):
    """a ClusterError raised when a node pool with the same name is added twice."""


class InvalidVersionError(ClusterError):
    """a ClusterError raised for a malformed Kubernetes version string."""


# ---------------------------------------------------------------------------
# 2. Dataclasses
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class NodePool:
    name: str
    size: int
    machine_type: str = "standard"

    def __post_init__(self) -> None:
        if self.size < 1:
            raise ValueError(f"Node pool {self.name!r} needs at least 1 node, got {self.size}")


@dataclass
class Cluster:
    name: str
    k8s_version: str
    node_pools: list[NodePool] = field(default_factory=list)

    @property
    def total_nodes(self) -> int:
        return sum(pool.size for pool in self.node_pools)

    def add_pool(self, pool: NodePool) -> None:
        if any(existing_pool.name == pool.name for existing_pool in self.node_pools):
            raise DuplicatePoolError(
                f"Node pool {pool.name!r} already exists in cluster {self.name!r}"
            )
        self.node_pools.append(pool)


# ---------------------------------------------------------------------------
# 3. Typing + string parsing
# ---------------------------------------------------------------------------
def parse_version(version: str) -> tuple[int, int, int]:
    """Parse "1.29.3" or "v1.29.3" into (1, 29, 3).

    Raise InvalidVersionError for anything else ("1.29", "abc", "1.x.3").
    """
    str_version = version.removeprefix("v")
    sp_version = str_version.split(".")
    if len(sp_version) != 3 or not all(part.isdecimal() for part in sp_version):
        raise InvalidVersionError(f"Version {version!r} is not a valid version")
    major, minor, patch = map(int, sp_version)
    return major, minor, patch


def can_upgrade(current: str, target: str) -> bool:
    """Kubernetes upgrade rule: same major, and either
    - one minor version up (1.29.x -> 1.30.y), or
    - same minor with a higher patch (1.29.3 -> 1.29.5).
    Everything else (skipping minors, downgrades, same version) is False.
    """
    cmajor, cminor, cpatch = parse_version(current)
    tmajor, tminor, tpatch = parse_version(target)
    if cmajor != tmajor:
        return False
    return tminor == cminor + 1 or (tminor == cminor and tpatch > cpatch)


# ---------------------------------------------------------------------------
# 4. Context managers + Protocol
# ---------------------------------------------------------------------------
class ClusterClient(Protocol):
    """Anything with these two methods counts as a client (given).

    This is Python's structural typing — like a C# interface, but a class
    doesn't have to declare that it implements it.
    """

    def create_cluster(self, name: str) -> Any: ...
    def delete_cluster(self, name: str) -> None: ...


@contextmanager
def temporary_cluster(client: ClusterClient, name: str) -> Iterator[Any]:
    """Create a cluster, yield it, and ALWAYS delete it afterwards —
    even if the code inside the `with` block raises.

        with temporary_cluster(client, "e2e-1") as cluster:
            ...
    """
    cluster = client.create_cluster(name)
    try:
        yield cluster
    finally:
        client.delete_cluster(name)


# ---------------------------------------------------------------------------
# 5. Polling helper (you'll reuse this for real API tests)
# ---------------------------------------------------------------------------
def wait_until(
    predicate: Callable[[], T],
    timeout: float = 30.0,
    interval: float = 1.0,
) -> T:
    """Call `predicate` every `interval` seconds until it returns something
    truthy, and return that value.

    Raise TimeoutError (built-in) if `timeout` seconds pass first.
    Hint: time.monotonic(), not time.time().
    """
    deadline = time.monotonic() + timeout
    while True:
        result = predicate()
        if result:
            return result
        if time.monotonic() > deadline:
            raise TimeoutError(f"Condition not met within {timeout!r} seconds")
        time.sleep(interval)


# ---------------------------------------------------------------------------
# 6. Comprehensions
# ---------------------------------------------------------------------------
def unhealthy_pods(pods: list[dict[str, Any]]) -> list[str]:
    """Return the names of pods that are not healthy, in input order.

    A pod is healthy only if status == "Running" AND ready is True.
    A missing "ready" key counts as not ready.
    Try to do it in one list comprehension.

        [{"name": "api-1", "status": "Running", "ready": True}, ...]
    """
    return [
        pod["name"] for pod in pods if not (pod.get("status") == "Running" and pod.get("ready"))
    ]
