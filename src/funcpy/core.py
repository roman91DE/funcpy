"""Core functional programming utilities."""

from collections.abc import Callable
from os import stat
from typing import TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


class List:
    @staticmethod
    def map(f: Callable[[A], B], xs: list[A]) -> list[B]:
        return [f(x) for x in xs]

    @staticmethod
    def filter(pred: Callable[[A], bool], xs: list[A]) -> list[A]:
        return [x for x in xs if pred(x)]

    @staticmethod
    def foldl(f: Callable[[B, A], B], acc: B, xs: list[A]) -> B:
        match xs:
            case [head, *rest]:
                return List.foldl(f, f(acc, head), rest)
            case _:
                return acc

    @staticmethod
    def reverse(xs: list[A]) -> list[A]:
        return List.foldl(lambda acc, x: [x] + acc, [], xs)

    @staticmethod
    def foldr(f: Callable[[A, B], B], acc: B, xs: list[A]) -> B:
        return List.foldl(Functions.swap(f), acc, List.reverse(xs))


class Functions:
    @staticmethod
    def swap(f: Callable[[A, B], C]) -> Callable[[B, A], C]:
        return lambda a, b: f(b, a)
