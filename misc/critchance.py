from decimal import Decimal, getcontext
from random import random
from time import sleep

getcontext().prec = 3


crits = []
crit_chance = Decimal(1 / 3)


for _ in range(25):
    is_crit = False
    current_crit_rate = Decimal(sum(crits) / len(crits)) if crits else Decimal(0)
    if current_crit_rate < crit_chance:
        is_crit = True
    elif current_crit_rate == crit_chance:
        print("RAND", end=" ")
        is_crit = random() < 0.5

    print(is_crit, f"{current_crit_rate:.3f}")
    crits.append(is_crit)
    sleep(0.25)
