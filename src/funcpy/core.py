"""Core functional programming utilities."""

import inspect
from collections.abc import Callable
from typing import Any, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


class List:
    """Functional operations for Python lists."""
    
    @staticmethod
    def map(f: Callable[[A], B], xs: list[A]) -> list[B]:
        """Transform each element in a list by applying a function.
        
        Example:
            List.map(lambda x: x * 2, [1, 2, 3]) -> [2, 4, 6]
        """
        return [f(x) for x in xs]

    @staticmethod
    def filter(pred: Callable[[A], bool], xs: list[A]) -> list[A]:
        """Keep only elements that satisfy a condition.
        
        Example:
            List.filter(lambda x: x % 2 == 0, [1, 2, 3, 4]) -> [2, 4]
        """
        return [x for x in xs if pred(x)]

    @staticmethod
    def foldl(f: Callable[[B, A], B], acc: B, xs: list[A]) -> B:
        """Combine all elements of a list with a function, starting from the left.
        
        The accumulator starts with the initial value and is updated by applying
        the function to the accumulator and each element in sequence.
        
        Example:
            List.foldl(lambda acc, x: acc + x, 0, [1, 2, 3]) -> 6  # (((0 + 1) + 2) + 3)
        """
        match xs:
            case [head, *rest]:
                return List.foldl(f, f(acc, head), rest)
            case _:
                return acc

    @staticmethod
    def reverse(xs: list[A]) -> list[A]:
        """Reverse the order of elements in a list.
        
        Example:
            List.reverse([1, 2, 3]) -> [3, 2, 1]
        """
        return List.foldl(lambda acc, x: [x] + acc, [], xs)

    @staticmethod
    def foldr(f: Callable[[A, B], B], acc: B, xs: list[A]) -> B:
        """Combine all elements of a list with a function, starting from the right.
        
        Similar to foldl but works from right to left, which can give different 
        results for non-commutative operations (like subtraction or division).
        
        Example:
            List.foldr(lambda x, acc: x - acc, 0, [1, 2, 3]) -> 2  # (1 - (2 - (3 - 0)))
        """
        return List.foldl(Functions.swap(f), acc, List.reverse(xs))


class Dict:
    """Functional operations for Python dictionaries."""

    @staticmethod
    def vmap(f: Callable[[A], B], d: dict[C, A]) -> dict[C, B]:
        """Transform the values in a dictionary while keeping the keys the same.
        
        Example:
            Dict.vmap(lambda v: v * 2, {'a': 1, 'b': 2}) -> {'a': 2, 'b': 4}
        """
        return {k: f(v) for (k,v) in d.items()}
    
    @staticmethod
    def kmap(f: Callable[[A], B], d: dict[A, C]) -> dict[B, C]:
        """Transform the keys in a dictionary while keeping the values the same.
        
        Example:
            Dict.kmap(lambda k: k.upper(), {'a': 1, 'b': 2}) -> {'A': 1, 'B': 2}
        """
        return {f(k): v for (k,v) in d.items()}
    
    @staticmethod
    def vfilter(pred: Callable[[A], bool], d: dict[B, A]) -> dict[B, A]:
        """Keep only dictionary entries where the value passes a test.
        
        Example:
            Dict.vfilter(lambda v: v > 1, {'a': 1, 'b': 2}) -> {'b': 2}
        """
        return {k: v for (k,v) in d.items() if pred(v)}
    
    @staticmethod
    def kfilter(pred: Callable[[A], bool], d: dict[A, B]) -> dict[A, B]:
        """Keep only dictionary entries where the key passes a test.
        
        Example:
            Dict.kfilter(lambda k: k in ['a', 'c'], {'a': 1, 'b': 2}) -> {'a': 1}
        """
        return {k: v for (k,v) in d.items() if pred(k)}



class Str:
    """Functional operations for Python strings."""

    @staticmethod
    def map(f: Callable[[str], str], s: str) -> str:
        """Transform each character in a string by applying a function.
        
        Example:
            Str.map(lambda c: c.upper(), "hello") -> "HELLO"
        """
        return "".join(f(c) for c in s)

    @staticmethod
    def filter(pred: Callable[[str], bool], s: str) -> str:
        """Keep only characters in a string that satisfy a condition.
        
        Example:
            Str.filter(lambda c: c in "aeiou", "hello") -> "eo"
        """
        return "".join(c for c in s if pred(c))

    @staticmethod
    def foldl(f: Callable[[B, str], B], acc: B, s: str) -> B:
        """Combine all characters of a string with a function, starting from the left.
        
        Example:
            Str.foldl(lambda acc, c: acc + c.upper(), "", "hello") -> "HELLO"
        """
        for c in s:
            acc = f(acc, c)
        return acc

    @staticmethod
    def foldr(f: Callable[[str, B], B], acc: B, s: str) -> B:
        """Combine all characters of a string with a function, starting from the right.
        
        Example:
            Str.foldr(lambda c, acc: c.upper() + acc, "", "hello") -> "OLLEH"
        """
        for c in reversed(s):
            acc = f(c, acc)
        return acc

    @staticmethod
    def reverse(s: str) -> str:
        """Reverse a string.
        
        Example:
            Str.reverse("hello") -> "olleh"
        """
        return s[::-1]




class Functions:
    """Utility functions for working with functions."""
    
    @staticmethod
    def swap(f: Callable[[A, B], C]) -> Callable[[B, A], C]:
        """Reverse the order of arguments to a function.
        
        Creates a new function that calls the original function
        with arguments in reverse order.
        
        Example:
            subtract = lambda a, b: a - b
            swap_subtract = Functions.swap(subtract)
            subtract(5, 3) -> 2
            swap_subtract(5, 3) -> -2  # Equivalent to subtract(3, 5)
        """
        return lambda a, b: f(b, a)

    @staticmethod
    def compose(f: Callable[[B], C], g: Callable[[A], B]) -> Callable[[A], C]:
        """Compose two functions into a new function.

        Creates a new function that applies ``g`` first, then ``f`` to the result.
        Equivalent to ``f(g(x))``.

        Example:
            add_one = lambda x: x + 1
            double = lambda x: x * 2
            Functions.compose(double, add_one)(3)  # (3 + 1) * 2 = 8
        """
        return lambda x: f(g(x))

    @staticmethod
    def pipe(value: Any, *fns: Callable[[Any], Any]) -> Any:
        """Pipe a value through a series of transformations.

        Applies each function in order, passing the result of each as input
        to the next.

        Example:
            Functions.pipe(3, lambda x: x + 1, lambda x: x * 2)  # (3 + 1) * 2 = 8
        """
        result: Any = value
        for f in fns:
            result = f(result)
        return result

    @staticmethod
    def curry(f: Callable[..., Any]) -> Callable[..., Any]:
        """Curry a function for partial application.

        Returns a chain of single-argument functions that collect arguments
        one at a time. Once all required arguments are provided, the original
        function is called.

        Example:
            add = Functions.curry(lambda x, y: x + y)
            add_five = add(5)
            add_five(10)  # 15
        """
        sig = inspect.signature(f)
        n = len([
            p for p in sig.parameters.values()
            if p.default is inspect.Parameter.empty
            and p.kind in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            )
        ])

        def _curry(args: tuple[Any, ...]) -> Callable[..., Any]:
            def inner(*new_args: Any) -> Any:
                all_args = args + new_args
                if len(all_args) >= n:
                    return f(*all_args)
                return _curry(all_args)
            return inner

        return _curry(())


compose = Functions.compose
pipe = Functions.pipe
curry = Functions.curry
