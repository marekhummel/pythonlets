from math import floor, sqrt

limit = 100

for i in range(1, limit + 1):
    ip = floor(sqrt(i))
    a = ip + (i - ip**2) / (ip * 2)
    off = a - sqrt(i)
    if ip == sqrt(i):
        print()
    print(f"{i}:\t\t{round(sqrt(i), 3)}\t\t{round(a, 3)}\t\t{round(off, 3)}")
