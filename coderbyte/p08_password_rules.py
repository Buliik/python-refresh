"""Problem 8: BUG HUNT, the system under test  (don't edit this file)

password_ok(pw) returns True only if ALL of these hold:

1. Length is 8 to 64 characters (inclusive).
2. It contains at least one digit (0-9).
3. It contains at least one uppercase letter.
4. It contains at least one lowercase letter.
5. It contains no whitespace (spaces, tabs, newlines).

Your task is in p08_test_password.py.
The CB_BUG checks below are how run.py plants bugs; ignore them while reading.
"""

import os


def _bug(name: str) -> bool:
    return os.environ.get("CB_BUG") == name


def password_ok(pw: str) -> bool:
    min_len = 7 if _bug("min_length_off_by_one") else 8
    if len(pw) < min_len:
        return False
    if len(pw) > 64 and not _bug("no_max_length"):
        return False
    if not any(c.isdigit() for c in pw) and not _bug("digit_not_required"):
        return False
    if not any(c.isupper() for c in pw):
        return False
    if not _bug("lowercase_not_required") and not any(c.islower() for c in pw):
        return False
    if _bug("only_spaces_checked"):
        return " " not in pw
    return not any(c.isspace() for c in pw)
