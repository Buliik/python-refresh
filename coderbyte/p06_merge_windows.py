"""Problem 6: Merge maintenance windows  (medium, 25 minutes)

You get a list of maintenance windows as [start, end] pairs of integers, in any
order (start <= end). Merge windows that overlap or touch (one ends exactly
where the next starts), and return the result sorted by start.

Examples:
    [[1, 3], [2, 6], [8, 10]]  ->  [[1, 6], [8, 10]]
    [[5, 7], [1, 2]]           ->  [[1, 2], [5, 7]]
    []                         ->  []

Run:  uv run python coderbyte/run.py 6
"""


def merge_windows(windows: list[list[int]]) -> list[list[int]]:
    merged = []
    for start, end in sorted(windows):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


SAMPLES = [
    ([[1, 3], [2, 6], [8, 10]], [[1, 6], [8, 10]]),
    ([[5, 7], [1, 2]], [[1, 2], [5, 7]]),
    ([], []),
]
