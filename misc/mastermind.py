from itertools import product


# ** Puzzle settings **

# Domain (and codomain) values
domain_values = ['red', 'green', 'white', 'blue', 'yellow', 'black', 'orange', 'purple']  # noqa

# Length of solution
image_size = 4

# Can solution contain duplicate values ?
duplicates = True

# values, correct value and place, correct value wrong place
guesses = [
    (['red', 'red', 'white', 'white'], 0, 0),
    (['blue', 'green', 'yellow', 'black'], 0, 2),
    (['orange', 'blue', 'green', 'purple'], 1, 1),
    (['orange', 'black', 'blue', 'orange'], 0, 2),
    (['yellow', 'blue', 'orange', 'blue'], 1, 1)
]


# -> 3-Digit-Lock
# domain_values = [str(i) for i in range(10)]
# image_size = 3
# duplicates = True
# guesses = [
#     ('291', 1, 0),
#     ('245', 0, 1),
#     ('463', 0, 2),
#     ('578', 0, 0),
#     ('569', 0, 1),
# ]


# *************************************************************


def eval_hints(guess, solution):
    no_rplaces = len([p for (i, p) in enumerate(guess) if p == solution[i]])
    no_rvalues = len(set(guess).intersection(set(solution)))

    # Since every right place is also a right value
    # Caviat: Double colors ?
    return (no_rplaces, no_rvalues-no_rplaces)


def main():
    def is_set(tpl):
        return len(set(tpl)) == len(tpl)

    # Create complete image space (reduced if duplicates are not allowed)
    combs = [
        tpl
        for tpl in product(domain_values, repeat=image_size)
        if (duplicates or is_set(tpl))
    ]

    # Reduce solution space by checking possible solution against given hints
    for values, *hints in guesses:
        combs = [c for c in combs if eval_hints(values, c) == tuple(hints)]

    # Print solutions
    print(f'Possible solutions: {len(combs)}')
    for c in combs:
        print(f'  {c}')


if __name__ == '__main__':
    main()
