from random import randint, random


# Line of N holes
# Rabbit hides in one of them
# You are able to check one hole at the time
# After every check, the rabbit hops one hole either to the left or the right
# Find the rabbit


N = 100


def step(n):
    direction = 1 if random() >= 0.5 else -1
    print(f'Rabbit moves to {n + direction}')
    return n + direction


def find(rabbit):
    for i in range(N):
        print(f'Checking {i}')
        if rabbit == i:
            return i
        rabbit = step(rabbit)

    for i in range(1, N):
        print(f'Checking {i}')
        if rabbit == i:
            return i
        rabbit = step(rabbit)

    return -1


if __name__ == '__main__':
    rabbit = randint(0, N-1)
    print(f'Rabbit starts at {rabbit}')
    print(f'Found rabbit at {find(rabbit)}')
