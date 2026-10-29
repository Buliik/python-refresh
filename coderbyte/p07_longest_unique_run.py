"""Problem 7 (stretch): Longest run without repeats  (medium-hard, 25 minutes)

Return the length of the longest substring of `s` (consecutive characters)
in which no character repeats.

Examples:
    "clusterpool"  ->  9     ("lusterpoo" has a repeat; "clusterpo" doesn't)
    "kubernetes"   ->  6
    "bbbb"         ->  1
    ""             ->  0

A simple solution checks every substring. That's fine to start with; then try
to do it in a single pass ("sliding window").

Run:  uv run python coderbyte/run.py 7
"""


def longest_unique_run(s: str) -> int:
    # your code here
    raise NotImplementedError


SAMPLES = [
    ("clusterpool", 9),
    ("kubernetes", 6),
    ("bbbb", 1),
    ("", 0),
]
