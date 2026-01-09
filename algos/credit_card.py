# https://www.youtube.com/watch?v=yaoSdFAL4UY&ab_channel=KevinLubick


class Luhn:
    """
    Luhn Algorithm
    Usually last digit is for check to fulfill criterion.
    Detects all single digit errors and almost all (98%) transposition errors.
    """

    def validate(self, cc: str) -> bool:
        return self._compute_total(cc) % 10 == 0

    def compute(self, cc: str) -> int:
        total = self._compute_total(cc)
        if len(cc) & 1:
            return (total // 10 + 1) * 10 - total
        else:
            if total & 1:
                return None
            return ((total // 10 + 1) * 10 - total) // 2

    def _compute_total(self, cc: str) -> int:
        digits = [int(d) for d in cc]
        doubled = [d if i & 1 else 2 * d for i, d in enumerate(digits)]

        return sum(d if d < 10 else 1 + (d % 10) for d in doubled)


class VerhoeffGumm:
    """
    Verhoeff Gumm Algorithm
    Based on group theory (D5 group), detects all single digit and transpositions errors.
    """

    D5_Element = tuple[int, int]

    def validate(self, cc: str) -> bool:
        combined = self._compute_total(cc)
        return combined == (1, 0)

    def compute(self, cc: str) -> int:
        combined = self._compute_total(cc)
        f, r = self._inverse(combined)
        return (0 if f == 1 else 5) + r

    def _d5(self, d: int) -> D5_Element:
        # Tuple in terms of pentagons: first item indicates the flip, second the rotation
        return (1 if d < 5 else -1, d % 5)

    def _operation(self, first: D5_Element, second: D5_Element) -> D5_Element:
        f, r = first
        g, s = second
        return (f * g, f * s + r)

    def _substitution(self, d: D5_Element) -> D5_Element:
        a, b = 2, -2
        f, r = d
        return (f, f * (a - r) + b)

    def _inverse(self, d: D5_Element) -> D5_Element:
        f, r = d
        return (f, r if f == -1 else [0, 4, 3, 2, 1][r])

    def _compute_total(self, cc: str) -> D5_Element:
        digits = [self._d5(int(d)) for d in cc]
        precomp = [self._substitution(d) if i & 1 else d for i, d in enumerate(digits)]

        combined = precomp[-1]
        for d in precomp[-2::-1]:
            combined = self._operation(d, combined)
        return combined


card_number = "6524742383249082"
luhn = Luhn()
vg = VerhoeffGumm()

print(luhn.compute(card_number[:-1]))
print(luhn.validate(card_number))

print(vg.compute("3529"))
print(vg.validate("35293"))
print(vg.compute(card_number[:-1]))
print(vg.validate(card_number))
