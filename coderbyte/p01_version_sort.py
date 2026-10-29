"""Problem 1: Version sort  (easy, 15 minutes)

Given a list of version strings in the form "MAJOR.MINOR.PATCH" (only digits,
no prefix), return them sorted from oldest to newest.

Compare versions by number, not as text: "1.10.0" is newer than "1.9.2".
Keep duplicates.

Examples:
    ["1.10.0", "1.9.2", "1.2.10"]  ->  ["1.2.10", "1.9.2", "1.10.0"]
    ["2.0.0", "1.0.0"]             ->  ["1.0.0", "2.0.0"]
    []                             ->  []

Run:  uv run python coderbyte/run.py 1
"""

from python_refresh.cluster import parse_version


def version_sort(versions: list[str]) -> list[str]:
    return sorted(versions, key=lambda v: tuple(int(part) for part in v.split(".")))


SAMPLES = [
    (["1.10.0", "1.9.2", "1.2.10"], ["1.2.10", "1.9.2", "1.10.0"]),
    (["2.0.0", "1.0.0"], ["1.0.0", "2.0.0"]),
    ([], []),
]
