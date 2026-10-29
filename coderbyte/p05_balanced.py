"""Problem 5: Balanced brackets  (medium, 20 minutes)

Return True if every bracket in `s` is closed by the matching bracket in the
correct order. Bracket pairs: (), [] and {}. Ignore all other characters.

Examples:
    "a(b[c]d)e"  ->  True
    "(]"         ->  False
    ""           ->  True

Run:  uv run python coderbyte/run.py 5
"""


def is_balanced(s: str) -> bool:
    """Return True if every bracket in `s` is closed by the matching bracket in
    the correct order. Bracket pairs: (), [] and {}. Ignore all other characters.
    """
    stack = []
    brackets = {")": "(", "]": "[", "}": "{"}

    for char in s:
        if char in brackets.values():
            stack.append(char)
        elif char in brackets.keys():
            if not stack or stack.pop() != brackets[char]:
                return False

    return not stack


SAMPLES = [
    ("a(b[c]d)e", True),
    ("(]", False),
    ("", True),
]
