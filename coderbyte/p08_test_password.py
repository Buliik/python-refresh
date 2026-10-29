"""Problem 8: BUG HUNT  (40 minutes)

The spec is in p08_password_rules.py. Write pytest tests for password_ok() here.

run.py plants 5 realistic bugs in password_ok(), one at a time. Your tests must
pass on the correct version and fail on each buggy one. Think like a tester:
one or more cases per rule, boundaries on both sides, valid and invalid input.

Run:  uv run python coderbyte/run.py 8
"""

import pytest
from p08_password_rules import password_ok

VALID = "Abcdefg1"


def test_baseline_is_valid():
    assert password_ok(VALID)


# Rule 1: Length is 8 to 64 characters (inclusive).
@pytest.mark.parametrize(
    ("pw", "expected"),
    [
        pytest.param("Abcdef1", False, id="7-too-short"),
        pytest.param("Abcdefg1", True, id="8-min-ok"),
        pytest.param("A" * 62 + "a" + "1", True, id="64-max-ok"),
        pytest.param("A" * 63 + "a" + "1", False, id="65-too-long"),
    ],
)
def test_length(pw, expected):
    assert password_ok(pw) is expected


# Rule 2: It contains at least one digit (0-9).
@pytest.mark.parametrize(
    ("pw", "expected"),
    [
        pytest.param("Abcdefgh", False, id="no-digit"),
        pytest.param("Abcdefg1", True, id="trailing-digit"),
        pytest.param("1Abcdefg", True, id="leading-digit"),
        pytest.param("a1234567890B", True, id="has-digits-middle"),
    ],
)
def test_digit(pw, expected):
    assert password_ok(pw) is expected


# Rule 3: It contains at least one uppercase letter.
@pytest.mark.parametrize(
    ("pw", "expected"),
    [
        pytest.param("abcdefg1", False, id="no-uppercase"),
        pytest.param("Abcdefg1", True, id="leading-uppercase"),
        pytest.param("1abcdefG", True, id="trailing-uppercase"),
    ],
)
def test_uppercase(pw, expected):
    assert password_ok(pw) is expected


# Rule 4: It contains at least one lowercase letter.
@pytest.mark.parametrize(
    ("pw", "expected"),
    [
        pytest.param("ABCDEFG1", False, id="no-lowercase"),
        pytest.param("Abcdefg1", True, id="middle-lowercase"),
        pytest.param("aBcdefG1", True, id="leading-lowercase"),
        pytest.param("ABCDEFG1a", True, id="trailing-lowercase"),
    ],
)
def test_lowercase(pw, expected):
    assert password_ok(pw) is expected


# Rule 5: It contains no whitespace (spaces, tabs, newlines).
@pytest.mark.parametrize(
    ("pw", "expected"),
    [
        pytest.param("Abc defg1", False, id="space"),
        pytest.param("\tAbcdefg1", False, id="tab-leading"),
        pytest.param("Abcdefg1\n", False, id="newline-trailing"),
        pytest.param("Abcdefg1", True, id="no-whitespace"),
    ],
)
def test_whitespace(pw, expected):
    assert password_ok(pw) is expected
