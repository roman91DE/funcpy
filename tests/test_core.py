"""Tests for funcpy.core module."""

import funcpy.core as fp


def test_list_map():
    f = lambda x: x**2
    a = [1, 2, 3]
    got = fp.List.map(f, a)
    expected = list(map(f, a))

    assert got == expected


def test_list_map_empty():
    f = lambda x: x**2
    a = []
    got = fp.List.map(f, a)
    assert got == []


def test_list_filter():
    is_even = lambda x: x % 2 == 0
    a = [1, 2, 3, 4, 5, 6]
    got = fp.List.filter(is_even, a)
    expected = list(filter(is_even, a))

    assert got == expected


def test_list_filter_empty():
    is_positive = lambda x: x > 0
    a = []
    got = fp.List.filter(is_positive, a)
    assert got == []


def test_list_filter_no_matches():
    is_negative = lambda x: x < 0
    a = [1, 2, 3]
    got = fp.List.filter(is_negative, a)
    assert got == []


def test_list_foldl():
    add = lambda acc, x: acc + x
    a = [1, 2, 3, 4]
    got = fp.List.foldl(add, 0, a)
    assert got == 10  # 0 + 1 + 2 + 3 + 4 = 10


def test_list_foldl_empty():
    add = lambda acc, x: acc + x
    a = []
    got = fp.List.foldl(add, 0, a)
    assert got == 0  # Initial accumulator is returned


def test_list_foldl_string_concat():
    concat = lambda acc, x: acc + x
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
    divide = lambda x, acc: x / acc if acc != 0 else float("inf")
    a = [4, 2, 4]
    got = fp.List.foldr(divide, 64, a)
    assert got == 0.125


def test_list_foldr_vs_foldl():
    # Testing that foldr behaves differently than foldl for non-commutative operations
    subtract = lambda x, acc: x - acc  # for foldr
    subtract_foldl = lambda acc, x: acc - x  # for foldl

    a = [1, 2, 3]
    got_foldr = fp.List.foldr(
        subtract, 0, a
    )  # 1 - (2 - (3 - 0)) = 1 - (2 - 3) = 1 - (-1) = 2
    got_foldl = fp.List.foldl(subtract_foldl, 0, a)  # ((0 - 1) - 2) - 3 = -6

    assert got_foldr == 2
    assert got_foldl == -6
    assert got_foldr != got_foldl  # Demonstrating non-commutativity


def test_list_foldr_empty():
    add = lambda x, acc: x + acc
    a = []
    got = fp.List.foldr(add, 0, a)
    assert got == 0  # Initial accumulator is returned
