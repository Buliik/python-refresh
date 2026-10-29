"""Coderbyte-style checker.

    uv run python coderbyte/run.py 3        # check problem 3
    uv run python coderbyte/run.py all      # scoreboard for every problem

Like Coderbyte, you see the full result of the sample tests, but for hidden tests
only how many passed and a short label for each failure, never the input.
Don't open _hidden.py; it would spoil the hidden tests.
"""

import base64
import copy
import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

PROBLEMS = {
    1: ("p01_version_sort", "version_sort"),
    2: ("p02_first_unique", "first_unique"),
    3: ("p03_compress", "compress"),
    4: ("p04_error_summary", "error_summary"),
    5: ("p05_balanced", "is_balanced"),
    6: ("p06_merge_windows", "merge_windows"),
    7: ("p07_longest_unique_run", "longest_unique_run"),
    9: ("p09_flatten", "flatten"),
}

BUGS = {
    "min_length_off_by_one": "accepts 7-character passwords",
    "no_max_length": "accepts passwords longer than 64",
    "digit_not_required": "accepts passwords without a digit",
    "lowercase_not_required": "accepts passwords without a lowercase letter",
    "only_spaces_checked": "rejects spaces but accepts tabs and newlines",
}

TIMEOUT_SECONDS = 10  # per coding problem


def _same(a, b) -> bool:
    """Compare like an auto-grader: tuples and lists count as equal."""
    try:
        return json.loads(json.dumps(a)) == json.loads(json.dumps(b))
    except TypeError:
        return a == b


def _hidden(number: int) -> list:
    from _hidden import DATA

    return json.loads(base64.b64decode(DATA))[str(number)]


def check_problem(number: int) -> float:
    """Run samples and hidden tests in this process. Return the hidden score (0-1)."""
    module_name, func_name = PROBLEMS[number]
    module = importlib.import_module(module_name)
    func = getattr(module, func_name)
    print(f"Problem {number}: {func_name}\n")

    print("Sample tests:")
    for arg, expected in module.SAMPLES:
        try:
            got = func(copy.deepcopy(arg))
        except NotImplementedError:
            print("  Not implemented yet.")
            return 0.0
        except Exception as exc:
            print(f"  ERROR  {func_name}({arg!r}) raised {type(exc).__name__}: {exc}")
            continue
        if _same(got, expected):
            print(f"  PASS   {func_name}({arg!r})")
        else:
            print(f"  FAIL   {func_name}({arg!r})")
            print(f"         expected {expected!r}")
            print(f"         got      {got!r}")

    hidden = _hidden(number)
    failed = []
    for arg, expected, label in hidden:
        try:
            ok = _same(func(copy.deepcopy(arg)), expected)
        except Exception as exc:
            ok = False
            label = f"{label} (raised {type(exc).__name__})"
        if not ok:
            failed.append(label)

    passed = len(hidden) - len(failed)
    print(f"\nHidden tests: {passed}/{len(hidden)} passed")
    for label in failed:
        print(f"  FAIL   hidden test: {label}")
    score = passed / len(hidden)
    print(f"\nScore: {score:.0%}")
    return score


def check_bug_hunt() -> float:
    """Problem 8: run the user's tests against the correct and buggy versions."""
    print("Problem 8: bug hunt\n")
    test_file = HERE / "p08_test_password.py"

    def run_tests(bug: str | None) -> tuple[bool, int, str]:
        env = {k: v for k, v in os.environ.items() if k != "CB_BUG"}
        if bug:
            env["CB_BUG"] = bug
        cmd = [sys.executable, "-m", "pytest", str(test_file), "-q", "-p", "no:cacheprovider"]
        result = subprocess.run(cmd, env=env, cwd=HERE, capture_output=True, text=True, timeout=120)
        return result.returncode == 0, result.returncode, result.stdout

    passed, code, output = run_tests(None)
    if code == 5:
        print("No tests found yet. Write test functions in p08_test_password.py.")
        return 0.0
    if not passed:
        print("Your tests FAIL on the correct version, so a test is wrong:\n")
        print(output[-2000:])
        return 0.0
    print("Correct version: your tests pass.\n")

    caught = 0
    for bug, description in BUGS.items():
        ok, _, _ = run_tests(bug)
        if ok:
            print(f"  SURVIVED  {description}")
        else:
            caught += 1
            print(f"  caught    {description}")
    score = caught / len(BUGS)
    print(f"\n{caught}/{len(BUGS)} bugs caught. Score: {score:.0%}")
    return score


def run_isolated(number: int) -> float | None:
    """Run one problem in a child process, so an infinite loop can't hang everything."""
    cmd = [sys.executable, str(Path(__file__)), "--inner", str(number)]
    timeout = 180 if number == 8 else TIMEOUT_SECONDS
    try:
        result = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f"Problem {number}: stopped after {timeout}s (infinite loop?).")
        return None
    lines = result.stdout.splitlines()
    score = None
    if lines and lines[-1].startswith("__SCORE__ "):
        score = float(lines.pop().split()[1])
    print("\n".join(lines))
    if result.returncode != 0:
        print(result.stderr[-3000:])
    return score


def main() -> int:
    args = sys.argv[1:]
    if args[:1] == ["--inner"]:
        number = int(args[1])
        score = check_bug_hunt() if number == 8 else check_problem(number)
        print(f"__SCORE__ {score}")
        return 0

    if not args:
        print(__doc__)
        return 0

    numbers = sorted([*PROBLEMS, 8]) if args[0] == "all" else [int(args[0])]
    scores = {}
    for number in numbers:
        if number not in PROBLEMS and number != 8:
            print(f"There is no problem {number}.")
            return 1
        scores[number] = run_isolated(number)
        print("-" * 60)

    if len(numbers) > 1:
        print("\nScoreboard:")
        for number, score in scores.items():
            shown = "no score (see output above)" if score is None else f"{score:.0%}"
            print(f"  Problem {number}: {shown}")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    sys.exit(main())
