"""Tests for funcpy.core module."""

import funcpy.core as fp
from funcpy.core import compose, curry, pipe


def test_list_map():
    def f(x):
        return x**2
    a = [1, 2, 3]
    got = fp.List.map(f, a)
    expected = list(map(f, a))

    assert got == expected


def test_list_map_empty():
    def f(x):
        return x**2
    a = []
    got = fp.List.map(f, a)
    assert got == []


def test_list_filter():
    def is_even(x):
        return x % 2 == 0
    a = [1, 2, 3, 4, 5, 6]
    got = fp.List.filter(is_even, a)
    expected = list(filter(is_even, a))

    assert got == expected


def test_list_filter_empty():
    def is_positive(x):
        return x > 0
    a = []
    got = fp.List.filter(is_positive, a)
    assert got == []


def test_list_filter_no_matches():
    def is_negative(x):
        return x < 0
    a = [1, 2, 3]
    got = fp.List.filter(is_negative, a)
    assert got == []


def test_list_foldl():
    def add(acc, x):
        return acc + x
    a = [1, 2, 3, 4]
    got = fp.List.foldl(add, 0, a)
    assert got == 10  # 0 + 1 + 2 + 3 + 4 = 10


def test_list_foldl_empty():
    def add(acc, x):
        return acc + x
    a = []
    got = fp.List.foldl(add, 0, a)
    assert got == 0  # Initial accumulator is returned


def test_list_foldl_string_concat():
    def concat(acc, x):
        return acc + x
    a = ["a", "b", "c"]
    got = fp.List.foldl(concat, "", a)
    assert got == "abc"


def test_list_reverse():
    a = [1, 2, 3, 4, 5]
    got = fp.List.reverse(a)
    expected = a[::-1]
    assert got == expected


def test_list_reverse_empty():
    a = []
    got = fp.List.reverse(a)
    assert got == []


def test_list_foldr():
    # Testing right fold with division (non-commutative operation)
    # For foldr: [4, 2, 4] with acc=64 should compute:
    # foldr(/, 64, [4, 2, 4]) = 4 / (2 / (4 / 64)) = 4 / (2 / 0.0625) = 4 / 32 = 0.125
    def divide(x, acc):
        return x / acc if acc != 0 else float("inf")
    a = [4, 2, 4]
    got = fp.List.foldr(divide, 64, a)
    assert got == 0.125


def test_list_foldr_vs_foldl():
    # Testing that foldr behaves differently than foldl for non-commutative operations
    def subtract(x, acc):
        return x - acc  # for foldr
    def subtract_foldl(acc, x):
        return acc - x  # for foldl

    a = [1, 2, 3]
    got_foldr = fp.List.foldr(
        subtract, 0, a
    )  # 1 - (2 - (3 - 0)) = 1 - (2 - 3) = 1 - (-1) = 2
    got_foldl = fp.List.foldl(subtract_foldl, 0, a)  # ((0 - 1) - 2) - 3 = -6

    assert got_foldr == 2
    assert got_foldl == -6
    assert got_foldr != got_foldl  # Demonstrating non-commutativity


def test_list_foldr_empty():
    def add(x, acc):
        return x + acc
    a = []
    got = fp.List.foldr(add, 0, a)
    assert got == 0  # Initial accumulator is returned


# String tests
def test_str_map():
    """Test Str.map function."""
    s = "hello"
    result = fp.Str.map(lambda c: c.upper(), s)
    assert result == "HELLO"
    
    # Empty string
    assert fp.Str.map(lambda c: c.upper(), "") == ""
    
    # Single character
    assert fp.Str.map(lambda c: c.upper(), "a") == "A"
    
    # Special characters
    assert fp.Str.map(lambda c: c + c, "abc") == "aabbcc"


def test_str_filter():
    """Test Str.filter function."""
    s = "hello world"
    result = fp.Str.filter(lambda c: c not in " aeiou", s)
    assert result == "hllwrld"
    
    # Empty string
    assert fp.Str.filter(lambda c: c != "x", "") == ""
    
    # No matches
    assert fp.Str.filter(lambda c: c.isdigit(), "abcdef") == ""
    
    # All matches
    assert fp.Str.filter(lambda c: c.isalpha(), "abcdef") == "abcdef"


def test_str_foldl():
    """Test Str.foldl function."""
    s = "hello"
    
    # Count characters
    result = fp.Str.foldl(lambda acc, _: acc + 1, 0, s)
    assert result == 5
    
    # Build uppercase string
    result = fp.Str.foldl(lambda acc, c: acc + c.upper(), "", s)
    assert result == "HELLO"
    
    # Empty string
    assert fp.Str.foldl(lambda acc, c: acc + c, "start", "") == "start"
    
    # Calculate checksum
    result = fp.Str.foldl(lambda acc, c: acc + ord(c), 0, "abc")
    assert result == ord('a') + ord('b') + ord('c')


def test_str_foldr():
    """Test Str.foldr function."""
    s = "hello"
    
    # Build reversed uppercase string
    result = fp.Str.foldr(lambda c, acc: acc + c.upper(), "", s)
    assert result == "OLLEH"
    
    # Empty string
    assert fp.Str.foldr(lambda c, acc: c + acc, "end", "") == "end"
    
    # Concatenate with separator
    result = fp.Str.foldr(lambda c, acc: c + (":"+acc if acc else ""), "", "abc")
    assert result == "a:b:c"


def test_str_reverse():
    """Test Str.reverse function."""
    s = "hello"
    result = fp.Str.reverse(s)
    assert result == "olleh"
    
    # Empty string
    assert fp.Str.reverse("") == ""
    
    # Single character
    assert fp.Str.reverse("a") == "a"
    
    # Palindrome
    assert fp.Str.reverse("racecar") == "racecar"
    
    # Special characters
    assert fp.Str.reverse("!@#$") == "$#@!"


# Compose tests
def test_functions_compose():
    def add_one(x: int) -> int:
        return x + 1

    def double(x: int) -> int:
        return x * 2

    got = fp.Functions.compose(double, add_one)(3)
    expected = 8  # (3 + 1) * 2
    assert got == expected


def test_functions_compose_module_level():
    got = compose(str.upper, str.strip)("  hello  ")
    expected = "HELLO"
    assert got == expected


def test_functions_compose_different_types():
    got = compose(lambda x: x * 2, len)("hello")
    expected = 10
    assert got == expected


# Pipe tests
def test_functions_pipe():
    got = fp.Functions.pipe(
        3,
        lambda x: x + 1,
        lambda x: x * 2,
        lambda x: f"Result: {x}",
    )
    expected = "Result: 8"
    assert got == expected


def test_functions_pipe_module_level():
    got = pipe(10, lambda x: x - 3, lambda x: x * x)
    expected = 49
    assert got == expected


def test_functions_pipe_single_fn():
    got = pipe(5, lambda x: x + 1)
    expected = 6
    assert got == expected


def test_functions_pipe_no_fns():
    got = pipe(42)
    expected = 42
    assert got == expected


# Curry tests
def test_functions_curry():
    add = fp.Functions.curry(lambda x, y: x + y)
    add_five = add(5)
    got = add_five(10)
    expected = 15
    assert got == expected


def test_functions_curry_module_level():
    multiply = curry(lambda x, y: x * y)
    double = multiply(2)
    got = double(7)
    expected = 14
    assert got == expected


def test_functions_curry_three_args():
    add3 = curry(lambda x, y, z: x + y + z)
    got = add3(1)(2)(3)
    expected = 6
    assert got == expected


def test_functions_curry_all_at_once():
    add = curry(lambda x, y: x + y)
    got = add(3, 4)
    expected = 7
    assert got == expected


def test_functions_curry_partial_groups():
    add3 = curry(lambda x, y, z: x + y + z)
    got = add3(1, 2)(3)
    expected = 6
    assert got == expected

