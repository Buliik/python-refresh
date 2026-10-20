"""Warm-up exercises. Add new topics as separate modules next to this one."""


def fizzbuzz(n: int) -> str:
    """Return "Fizz", "Buzz", "FizzBuzz", or the number as a string."""
    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)


def is_palindrome(text: str) -> bool:
    """Check whether text reads the same backwards, ignoring case and non-letters."""
    cleaned = [c.lower() for c in text if c.isalnum()]
    return cleaned == cleaned[::-1]
