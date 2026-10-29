"""Problem 9: MOCK INTERVIEW: flatten a nested config  (40 minutes)

Do this one like the real thing: start a 40-minute timer, start a screen or
voice recording, and THINK OUT LOUD the whole time, as if an interviewer were
listening. Say your plan and your edge cases before you code.

Turn a nested dictionary into a flat one whose keys are the paths joined by
dots. Values that aren't dictionaries (numbers, strings, None, lists, ...)
are kept as they are.

Examples:
    {"a": 1, "b": {"c": 2, "d": {"e": 3}}}  ->  {"a": 1, "b.c": 2, "b.d.e": 3}
    {}                                      ->  {}
    {"x": [1, 2]}                           ->  {"x": [1, 2]}

Run:  uv run python coderbyte/run.py 9
"""


def flatten(data: dict) -> dict:
    # your code here
    raise NotImplementedError


SAMPLES = [
    ({"a": 1, "b": {"c": 2, "d": {"e": 3}}}, {"a": 1, "b.c": 2, "b.d.e": 3}),
    ({}, {}),
    ({"x": [1, 2]}, {"x": [1, 2]}),
]
