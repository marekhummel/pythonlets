# Disk with 4 rotable layers, each with numbers grouped in columns.
# Rotate disks so that sum along each column is equal

from itertools import repeat

ring1 = [3, 2, 3, 27, 20, 11, 27, 10, 19, 10, 13, 10, 2, 15, 23, 19]
ring2_low = [5, 1, 24, 2, 10, 9, 7, 3, 12, 24, 10, 9, 22, 9, 5, 10]
ring2_high = [2, 2, 10, 15, 6, 9, 16, 17]
ring3_low = [5, 7, 8, 24, 8, 3, 6, 15, 22, 6, 1, 1, 11, 27, 14, 5]
ring3_high = [5, 10, 2, 22, 2, 17, 15, 14]
ring4_low = [6, 3, 1, 6, 10, 6, 10, 2, 6, 10, 4, 1, 5, 5, 4, 8]
ring4_high = [10, 10, 10, 6, 13, 3, 3, 6]


columns = len(ring1)

ring2_high = [*sum(zip(ring2_high, repeat(None)), ())]
ring3_high = [*sum(zip(ring3_high, repeat(None)), ())]
ring4_high = [*sum(zip(ring4_high, repeat(None)), ())]


# print(len(ring1))
# print(len(ring2_low))
# print(len(ring3_low))
# print(len(ring4_low))
# print(len(ring2_high))
# print(len(ring3_high))
# print(len(ring4_high))


def rotate(l):
    return l[-1:] + l[:-1]


for rotation2 in range(columns):
    ring2_high = rotate(ring2_high)
    ring3_low = rotate(ring3_low)
    for rotation3 in range(columns):
        ring3_high = rotate(ring3_high)
        ring4_low = rotate(ring4_low)
        for rotation4 in range(columns):
            ring4_high = rotate(ring4_high)

            sums = [0] * columns
            for column in range(columns):
                sums[column] += ring1[column]
                sums[column] += ring2_high[column] or ring2_low[column]
                sums[column] += ring3_high[column] or ring3_low[column]
                sums[column] += ring4_high[column] or ring4_low[column]

            if all(s == sums[0] for s in sums):
                print(sums[0])
                print(ring1)
                print(ring2_high)
                print(ring3_high)
                print(ring4_high)
                exit(0)

print("Found nothing")
