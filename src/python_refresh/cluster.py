"""Day 1 — Python refresh.

Implement everything marked TODO, then run:

    uv run pytest tests/test_cluster.py -v

Work top to bottom; each section maps to one group of tests.
Requires Python 3.10+ (your project uses 3.13).
"""
from __future__ import annotations

import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Callable, Iterator, Protocol, TypeVar

T = TypeVar("T")


# ---------------------------------------------------------------------------
# 1. Exceptions
# ---------------------------------------------------------------------------
class ClusterError(Exception):
    """Base class for every error raised by this module (given)."""


# TODO: define DuplicatePoolError — a ClusterError raised when a node pool
#       with the same name is added twice.

# TODO: define InvalidVersionError — a ClusterError raised for a malformed
#       Kubernetes version string.


# ---------------------------------------------------------------------------
# 2. Dataclasses
# ---------------------------------------------------------------------------
# TODO: NodePool — an IMMUTABLE dataclass with fields:
#         name: str
#         size: int
#         machine_type: str = "standard"
#       Raise ValueError if size < 1 (hint: __post_init__).


# TODO: Cluster — a mutable dataclass with fields:
#         name: str
#         k8s_version: str
#         node_pools: list[NodePool]  — defaults to an empty list
#                                       (careful: each Cluster needs its own list)
#       Plus:
#         total_nodes  — read-only property, sum of all pool sizes
#         add_pool(pool) -> None — raises DuplicatePoolError if a pool
#                                  with the same name already exists


# ---------------------------------------------------------------------------
# 3. Typing + string parsing
# ---------------------------------------------------------------------------
def parse_version(version: str) -> tuple[int, int, int]:
    """Parse "1.29.3" or "v1.29.3" into (1, 29, 3).

    Raise InvalidVersionError for anything else ("1.29", "abc", "1.x.3").
    """
    raise NotImplementedError  # TODO


def can_upgrade(current: str, target: str) -> bool:
    """Kubernetes upgrade rule: same major, and either
    - one minor version up (1.29.x -> 1.30.y), or
    - same minor with a higher patch (1.29.3 -> 1.29.5).
    Everything else (skipping minors, downgrades, same version) is False.
    """
    raise NotImplementedError  # TODO


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
    raise NotImplementedError  # TODO
    yield  # keeps this a generator until you implement it


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
    raise NotImplementedError  # TODO


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
    raise NotImplementedError  # TODO
