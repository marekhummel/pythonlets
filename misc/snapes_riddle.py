# https://harrypotter.fandom.com/wiki/Potion_riddle

from enum import IntEnum
from itertools import permutations


class Potion(IntEnum):
    Poison = 0
    Wine = 1
    Backward = 2
    Forward = 3


start = [
    Potion.Poison,
    Potion.Poison,
    Potion.Poison,
    Potion.Wine,
    Potion.Wine,
    Potion.Backward,
    Potion.Forward,
]


solutions = set()
for setting in permutations(start):
    # Left to each wine is poison
    failed = False
    for i in range(1, len(setting)):
        if setting[i] == Potion.Wine and setting[i - 1] != Potion.Poison:
            failed = True

    if failed:
        continue

    # First and last are different and neither help to progress
    first, last = setting[0], setting[-1]
    if first == last or first == Potion.Forward or last == Potion.Forward:
        continue

    # Biggest (6th) and smallest (3rd) not poison
    biggest, smallest = setting[5], setting[2]
    if biggest == Potion.Poison or smallest == Potion.Poison:
        continue

    # 2nd from left and right are equal
    second_left, second_right = setting[1], setting[-2]
    if second_left != second_right:
        continue

    # valid
    solutions.add(setting)


for sol in solutions:
    print([s.name for s in sol])

# Solution
# Poison Wine Forward Poison Poison Wine Backward
