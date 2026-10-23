"""Day 2 fixtures.

pytest loads conftest.py automatically. Every fixture defined here is
available to every test in this folder by parameter name, with no import needed.
"""

import uuid
from collections.abc import Callable, Iterator
from contextlib import suppress

import pytest

from python_refresh.cluster import temporary_cluster
from python_refresh.taikun_fake import ClusterInfo, ClusterNotFoundError, FakeTaikunClient


#  1 — `run_id`, SESSION scope
#   Return a short unique string for this whole test run, e.g. "t3f9a1c".
#   Real shared environments need unique resource names, so parallel CI runs
#   don't collide. Cluster names must be lowercase letters, digits and "-",
#   and must start with a letter or digit.
#   Hint: uuid.uuid4().hex
@pytest.fixture(scope="session")
def run_id() -> str:
    return f"t{uuid.uuid4().hex[:6]}"


# 2 — `client`, FUNCTION scope (the default)
#   Return a fresh FakeTaikunClient. Use provisioning_polls=2 and quota=3.
#   Bonus question for later: what breaks if you make this session-scoped?
@pytest.fixture
def client() -> FakeTaikunClient:
    return FakeTaikunClient(provisioning_polls=2, quota=3)


# 3 — `cluster`
#   Depends on `client` and `run_id`. Create a cluster named f"{run_id}-basic"
#   using YOUR temporary_cluster() from Day 1, and yield it to the test.
#   Teardown is handled by temporary_cluster, so this is only a few lines.
@pytest.fixture
def cluster(client: FakeTaikunClient, run_id: str) -> Iterator[ClusterInfo]:
    with temporary_cluster(client, f"{run_id}-basic") as info:
        yield info


# 4 — `make_cluster`, a "factory fixture"
#   Depends on `client` and `run_id`. Yield a FUNCTION that tests call to create
#   as many clusters as they need:
#
#       def test_something(make_cluster):
#           a = make_cluster()              # auto-named, e.g. "t3f9a1c-1"
#           b = make_cluster(nodes=5)       # extra kwargs go to create_cluster
#
#   Remember every name you created. After the test (after `yield`), delete each
#   one that still exists. A test may already have deleted some, so ignore
#   ClusterNotFoundError.
@pytest.fixture
def make_cluster(client: FakeTaikunClient, run_id: str) -> Iterator[Callable[..., ClusterInfo]]:
    created_names: list[str] = []

    def _make_cluster(**kwargs) -> ClusterInfo:
        name = f"{run_id}-{len(created_names) + 1}"
        info = client.create_cluster(name=name, **kwargs)
        created_names.append(name)
        return info

    yield _make_cluster

    for name in created_names:
        with suppress(ClusterNotFoundError):
            client.delete_cluster(name)
