import pytest

from python_refresh.basics import fizzbuzz, is_palindrome


@pytest.mark.parametrize(
    ("n", "expected"),
    [(1, "1"), (3, "Fizz"), (5, "Buzz"), (15, "FizzBuzz"), (98, "98")],
)
def test_fizzbuzz(n, expected):
    assert fizzbuzz(n) == expected


def test_palindrome_ignores_case_and_punctuation():
    assert is_palindrome("A man, a plan, a canal: Panama")


def test_not_palindrome():
    assert not is_palindrome("python")
