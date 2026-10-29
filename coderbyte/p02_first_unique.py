"""Problem 2: First unique character  (easy, 15 minutes)

Return the index of the first character in `s` that appears exactly once.
Return -1 if there is no such character. Characters are case-sensitive,
and spaces count as characters.

Examples:
    "kubernetes"  ->  0     ("k" appears once)
    "aabbc"       ->  4
    "aabb"        ->  -1

Run:  uv run python coderbyte/run.py 2
"""

from collections import Counter


def first_unique(s: str) -> int:
    counts = Counter(s)
    for i, c in enumerate(s):
        if counts[c] == 1:
            return i
    return -1


SAMPLES = [
    ("kubernetes", 0),
    ("aabbc", 4),
    ("aabb", -1),
]
