from math import floor, sqrt

max = 100

for i in range(1, max + 1):
    ip = floor(sqrt(i))
    a = ip + (i - ip ** 2) / (ip * 2)
    off = a - sqrt(i)
    if ip == sqrt(i):
        print()
    print(
        "{0}:\t\t{1}\t\t{2}\t\t{3}".format(
            i, round(sqrt(i), 3), round(a, 3), round(off, 3)
        )
    )
