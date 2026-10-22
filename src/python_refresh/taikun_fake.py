"""A fake, in-memory Kubernetes cluster API — the system under test for Day 2.

DON'T EDIT THIS FILE. Your job is to test it.

It behaves like a (very) simplified Taikun API:

- Cluster names must be lowercase DNS labels: 1-40 chars of a-z, 0-9 and "-",
  not starting or ending with "-".  -> ValidationError
- A cluster has 1-100 nodes.  -> ValidationError
- Names are unique.  -> DuplicateClusterError
- At most `quota` clusters can exist at once.  -> QuotaExceededError
- Unknown names on get/delete/upgrade.  -> ClusterNotFoundError
- New clusters start as "PENDING" and become "RUNNING" after
  `provisioning_polls` calls to get_cluster() — like a real async API.
- Upgrades follow Kubernetes rules (one minor up, or a patch up) and need a
  RUNNING cluster.  -> UpgradeNotAllowedError / ClusterNotReadyError

tools/check_mutants.py plants bugs in this file via the TAIKUN_MUTANT
environment variable. Ignore the `_mutant(...)` checks while reading.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass

from python_refresh.cluster import can_upgrade

_NAME = re.compile(r"[a-z0-9]([a-z0-9-]{0,38}[a-z0-9])?")
MAX_NODES = 100


def _mutant(name: str) -> bool:
    return os.environ.get("TAIKUN_MUTANT") == name


class TaikunError(Exception):
    """Base class for every error this API raises."""


class ValidationError(TaikunError):
    """Invalid input, such as a bad name or node count."""


class DuplicateClusterError(TaikunError):
    """A cluster with this name already exists."""


class QuotaExceededError(TaikunError):
    """Creating another cluster would exceed the quota."""


class ClusterNotFoundError(TaikunError):
    """No cluster with this name exists."""


class ClusterNotReadyError(TaikunError):
    """The operation needs a RUNNING cluster."""


class UpgradeNotAllowedError(TaikunError):
    """The requested Kubernetes upgrade breaks the upgrade rules."""


@dataclass
class ClusterInfo:
    name: str
    k8s_version: str
    nodes: int
    status: str = "PENDING"


class FakeTaikunClient:
    def __init__(self, quota: int = 3, provisioning_polls: int = 2) -> None:
        self.quota = quota
        self.provisioning_polls = provisioning_polls
        self._clusters: dict[str, ClusterInfo] = {}
        self._polls: dict[str, int] = {}
        self._used_quota = 0

    # --- create / read -------------------------------------------------
    def create_cluster(self, name: str, k8s_version: str = "1.30.0", nodes: int = 1) -> ClusterInfo:
        if not _mutant("no_name_validation") and not _NAME.fullmatch(name):
            raise ValidationError(f"Invalid cluster name {name!r}")
        max_nodes = MAX_NODES + 1 if _mutant("nodes_upper_bound") else MAX_NODES
        if not 1 <= nodes <= max_nodes:
            raise ValidationError(f"Node count must be 1-{MAX_NODES}, got {nodes}")
        if name in self._clusters and not _mutant("duplicate_allowed"):
            raise DuplicateClusterError(f"Cluster {name!r} already exists")
        limit = self.quota + 1 if _mutant("quota_off_by_one") else self.quota
        if self._used_quota >= limit:
            raise QuotaExceededError(f"Quota of {self.quota} clusters reached")

        info = ClusterInfo(name=name, k8s_version=k8s_version, nodes=nodes)
        if name not in self._clusters:
            self._used_quota += 1
        self._clusters[name] = info
        self._polls[name] = 0
        return info

    def get_cluster(self, name: str) -> ClusterInfo:
        info = self._get(name)
        self._polls[name] += 1
        if (
            info.status == "PENDING"
            and self._polls[name] >= self.provisioning_polls
            and not _mutant("never_ready")
        ):
            info.status = "RUNNING"
        return info

    def list_clusters(self) -> list[ClusterInfo]:
        return list(self._clusters.values())

    # --- update / delete -----------------------------------------------
    def upgrade_cluster(self, name: str, target_version: str) -> ClusterInfo:
        info = self._get(name)
        if info.status != "RUNNING":
            raise ClusterNotReadyError(f"Cluster {name!r} is {info.status}, not RUNNING")
        allowed = can_upgrade(info.k8s_version, target_version)
        if _mutant("upgrade_skips_check"):
            allowed = target_version != info.k8s_version
        if not allowed:
            raise UpgradeNotAllowedError(f"Cannot upgrade {info.k8s_version} -> {target_version}")
        info.k8s_version = target_version
        return info

    def delete_cluster(self, name: str) -> None:
        if name not in self._clusters:
            if _mutant("delete_silent"):
                return
            raise ClusterNotFoundError(f"Cluster {name!r} not found")
        del self._clusters[name]
        del self._polls[name]
        if not _mutant("leaky_quota"):
            self._used_quota -= 1

    def _get(self, name: str) -> ClusterInfo:
        try:
            return self._clusters[name]
        except KeyError:
            raise ClusterNotFoundError(f"Cluster {name!r} not found") from None
