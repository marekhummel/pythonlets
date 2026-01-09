# Numberphile: https://www.youtube.com/watch?v=1MtEUErz7Gg
# Paper: https://fse.studenttheses.ub.rug.nl/21391/1/bMath_2020_DomanN.pdf
from typing import Self


class Sandpile:
    def __init__(self, values: list[int], size: int = 3) -> None:
        assert len(values) == size * size, f"Need {size * size} values for sandpile"
        assert all(0 <= x <= 3 for x in values), "Values may only range from 0 to 3"

        self.size = size
        self.values = values

    def __add__(self, other) -> Self:
        result = [x + y for x, y in zip(self.values, other.values)]
        while any(x > 3 for x in result):
            result = self._topple(result)

        return Sandpile(result)

    # def __neg__(self) -> Self | None:
    #     inv = ...
    #     return inv if self.derivable_from_threes() else None

    def derivable_from_threes(self) -> bool:
        zero = Sandpile([2, 1, 2, 1, 0, 1, 2, 1, 2])
        return self + zero == self

    def _topple(self, values) -> list[int]:
        for i, x in enumerate(values):
            if x <= 3:
                continue

            values[i] -= 4
            r, c = i // self.size, i % self.size
            if r > 0:
                values[(r - 1) * self.size + c] += 1
            if r < self.size - 1:
                values[(r + 1) * self.size + c] += 1
            if c > 0:
                values[r * self.size + (c - 1)] += 1
            if c < self.size - 1:
                values[r * self.size + (c + 1)] += 1

        return values

    def __eq__(self, other: object) -> bool:
        return self.values == other.values if isinstance(other, Sandpile) else False

    def __repr__(self) -> str:
        return repr(self.values)


a = Sandpile([2, 2, 0, 2, 1, 1, 0, 1, 3])
b = Sandpile([2, 1, 3, 1, 0, 1, 0, 1, 0])
print(a + b)

c = Sandpile([3, 3, 3, 3, 3, 3, 3, 3, 3])
d = Sandpile([0, 0, 0, 0, 1, 0, 0, 0, 0])
print(c + d)

e = Sandpile([2, 2, 2, 2, 2, 2, 2, 2, 2])
f = Sandpile([2, 1, 2, 1, 0, 1, 2, 1, 2])  # zero if e can be derived from all 3s
print(e + f)

print()

print(a, a.derivable_from_threes())
print(e, e.derivable_from_threes())
