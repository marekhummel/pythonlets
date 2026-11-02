"""A small, register-based FRACTRAN interpreter.

Programs are lists of (numerator, denominator) pairs. The exponent of each
prime in the current number is a register.
"""

from collections.abc import Callable, Iterator
from itertools import islice
from math import prod
from typing import Self

Rule = tuple[int, int]


class FTNum:
    """Prime-exponent registers used to encode a positive FRACTRAN number."""

    _values: dict[int, int] = {}

    def __init__(self, number: int) -> None:
        """Create registers containing the prime factors of number."""
        self._values = self._factorise(number)

    def prime_factors(self) -> list[int]:
        """Return the list of primes which have non-zero registers."""
        return [p for p in self._values if self._values[p] > 0]

    def exponent(self, prime: int) -> int:
        """Return the value of the register represented by prime."""
        return self._values.get(prime, 0)

    def can_divide(self, other: Self) -> bool:
        """Return whether every register in other can be subtracted."""
        return all(self.exponent(prime) >= exponent for prime, exponent in other._values.items())

    def multiply(self, other: Self) -> None:
        """Add the register values from other."""
        for prime, exponent in other._values.items():
            self._values[prime] = self.exponent(prime) + exponent

    def divide(self, other: Self) -> None:
        """Subtract the register values from other."""
        if not self.can_divide(other):
            raise ValueError("registers cannot be subtracted")

        for prime, exponent in other._values.items():
            self._values[prime] = self.exponent(prime) - exponent

    def to_int(self) -> int:
        """Encode the registers as a positive FRACTRAN number."""
        return prod(prime**exponent for prime, exponent in self._values.items())

    @staticmethod
    def _factorise(number: int) -> dict[int, int]:
        if number < 1:
            raise ValueError("FRACTRAN numbers must be positive")

        factors: dict[int, int] = {}
        prime = 2
        while prime * prime <= number:
            while number % prime == 0:
                factors[prime] = factors.get(prime, 0) + 1
                number //= prime
            prime += 1 if prime == 2 else 2
        if number > 1:
            factors[number] = factors.get(number, 0) + 1
        return factors


class Fractran:
    def __init__(self, program: list[Rule]):
        self.program = tuple(
            (FTNum(numerator), FTNum(denominator)) for numerator, denominator in program
        )

    def run[Out](
        self, initial: int, extract: Callable[[FTNum, bool], Out | None]
    ) -> Iterator[Out]:
        """Yield each non-None value returned by extract for the current number."""
        number = FTNum(initial)
        while True:
            is_final = True
            for numerator, denominator in self.program:
                if number.can_divide(denominator):
                    number.divide(denominator)
                    number.multiply(numerator)

                    is_final = False
                    break

            value = extract(number, is_final)
            if value is not None:
                yield value

            if is_final:
                break

    @classmethod
    def make_function[**P, Out](
        cls,
        program: list[Rule],
        encode: Callable[P, int],
        extract: Callable[[FTNum, bool], Out | None],
    ) -> Callable[P, Iterator[Out]]:
        """Build a generator function which yields conditional extracted values."""
        interpreter = cls(program)

        def compute(*args: P.args, **kwargs: P.kwargs) -> Iterator[Out]:
            return interpreter.run(encode(*args, **kwargs), extract)

        return compute


plus = Fractran.make_function(
    [(3, 2)],
    lambda a, b: 2**a * 3**b,
    lambda num, is_final: num.exponent(3) if is_final else None,
)

minus = Fractran.make_function(
    [(1, 6)],
    lambda a, b: 2**a * 3**b,
    lambda num, is_final: num.exponent(2) if is_final else None,
)

multiply = Fractran.make_function(
    [(455, 33), (11, 13), (1, 11), (3, 7), (11, 2), (1, 3)],
    lambda a, b: 2**a * 3**b,
    lambda num, is_final: num.exponent(5) if is_final else None,
)

divrem = Fractran.make_function(
    [(91, 66), (11, 13), (1, 33), (85, 11), (57, 119), (17, 19), (11, 17), (1, 3)],
    lambda n, d: 2**n * 3**d * 11,
    lambda num, is_final: (num.exponent(5), num.exponent(7)) if is_final else None,
)

double = Fractran.make_function(
    [(9, 2)],
    lambda a: 2**a,
    lambda num, is_final: num.exponent(3) if is_final else None,
)

max_ab = Fractran.make_function(
    [(5, 6), (5, 2), (5, 3)],
    lambda a, b: 2**a * 3**b,
    lambda num, is_final: num.exponent(5) if is_final else None,
)

fibonacci = Fractran.make_function(
    [(91, 33), (11, 13), (1, 11), (399, 34), (17, 19), (1, 17), (2, 7), (187, 5), (1, 3)],
    lambda n: 2 * 5 ** (n - 1),
    lambda num, is_final: num.exponent(2) if is_final else None,
)

primegame = Fractran.make_function(
    [
        (17, 91),
        (78, 85),
        (19, 51),
        (23, 38),
        (29, 33),
        (77, 29),
        (95, 23),
        (77, 19),
        (1, 17),
        (11, 13),
        (13, 11),
        (15, 2),
        (1, 7),
        (55, 1),
    ],
    lambda: 2,
    lambda num, _: num.exponent(2) if num.prime_factors() == [2] else None,
)


if __name__ == "__main__":
    print("Plus(10, 3) =", *plus(10, 3))
    print("Minus(10, 3) =", *minus(10, 3))
    print("Multiply(21, 8) =", *multiply(21, 8))
    print("Divrem(17, 5) =", *divrem(17, 5))
    print("Double(43) =", *double(43))
    print("Max(12, 17) =", *max_ab(12, 17))
    print("Fibonacci(10) =", *fibonacci(10))
    print("Prime Game =", *islice(primegame(), 10))
