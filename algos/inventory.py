# Numberphile: https://www.youtube.com/watch?v=rBU9E-ZOZAI

from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

inventory = defaultdict(lambda: 0)


def count_inventory():
    i = 0
    while True:
        current = inventory[i]
        inventory[current] += 1
        yield current

        if current == 0:
            break
        i += 1


data = []
while len(data) < 10000:
    data.extend(iter(count_inventory()))
print("done")


plt.plot(range(len(data)), data)
plt.grid()
plt.show()
