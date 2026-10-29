"""Problem 4: Error summary from logs  (medium, 25 minutes)

Each log line looks like:

    "<timestamp> <LEVEL> <service> <message...>"
    e.g. "2026-10-29T10:00:01 ERROR api Timeout calling db"

Fields are separated by whitespace. The message may contain spaces, or be missing.

Return a list of (service, error_count) tuples for every service with at least
one ERROR line, sorted by error_count (highest first), then by service name
(A-Z) when counts are equal.

Rules:
- Only the level "ERROR" counts (exact, case-sensitive).
- Ignore blank lines and lines with fewer than 3 fields.

Examples:
    ["t1 ERROR api Timeout", "t2 INFO api ok",
     "t3 ERROR db Down", "t4 ERROR api Timeout again"]  ->  [("api", 2), ("db", 1)]
    []                                                  ->  []
    ["t1 INFO web started"]                             ->  []

Run:  uv run python coderbyte/run.py 4
"""


def error_summary(lines: list[str]) -> list[tuple[str, int]]:
    """Return a list of (service, error_count) tuples for every service with at least
    one ERROR line, sorted by error_count (highest first), then by service name
    (A-Z) when counts are equal.
    """
    counts = {}
    for line in lines:
        parts = line.split(maxsplit=3)
        if len(parts) < 3:
            continue
        _, level, service, *_ = parts
        if level == "ERROR":
            counts[service] = counts.get(service, 0) + 1

    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))


SAMPLES = [
    (
        [
            "t1 ERROR api Timeout",
            "t2 INFO api ok",
            "t3 ERROR db Down",
            "t4 ERROR api Timeout again",
        ],
        [("api", 2), ("db", 1)],
    ),
    ([], []),
    (["t1 INFO web started"], []),
]
