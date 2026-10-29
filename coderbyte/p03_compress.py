"""Problem 3: Run-length encoding  (easy, 15 minutes)

Compress a string by replacing each run of the same character with the
character followed by the length of the run.

Examples:
    "aaabccdddd"  ->  "a3b1c2d4"
    "abc"         ->  "a1b1c1"
    ""            ->  ""

Run:  uv run python coderbyte/run.py 3
"""


def compress(s: str) -> str:
    if not s:
        return ""

    result = []
    count = 1
    prev_char = s[0]

    for char in s[1:]:
        if char == prev_char:
            count += 1
        else:
            result.append(f"{prev_char}{count}")
            prev_char = char
            count = 1

    result.append(f"{prev_char}{count}")

    return "".join(result)


SAMPLES = [
    ("aaabccdddd", "a3b1c2d4"),
    ("abc", "a1b1c1"),
    ("", ""),
]
