from itertools import product

# *********************
type Permuation[T] = tuple[T, ...]
type Guess[T] = tuple[Permuation[T], int, int]
type SolutionSpace[T] = list[Permuation[T]]
type ResponseSpace = list[tuple[int, int]]
# *********************


# -> 3-Digit-Lock
# DOMAIN = [str(i) for i in range(10)]
# IMAGE_SIZE = 3
# ALLOW_DUPLICATES = True
# GUESSES = [
#     ('291', 1, 0),
#     ('245', 0, 1),
#     ('463', 0, 2),
#     ('578', 0, 0),
#     ('569', 0, 1),
# ]


# ** Puzzle settings **
# Given the puzzle domains and the given guesses, evaluates the possible solutions

# Domain (and codomain) values
DOMAIN = ["red", "green", "white", "blue", "yellow", "purple"]

# Length of solution
IMAGE_SIZE = 3

# Can solution contain duplicate values ?
ALLOW_DUPLICATES = False

# Guesses done so far
GUESSES: list[Guess] = []


# *********************


def compute_next_guess[T](
    domain: list[T], solution_space: SolutionSpace[T], response_space: ResponseSpace
) -> Permuation[T]:
    best = None
    for g in solution_space:
        left = []
        for p, v in response_space:
            guess = (g, p, v)
            guess_list = GUESSES + [guess]
            possible = compute_solutions(domain, solution_space, guess_list)
            possible_space_size = len(possible)
            left.append(possible_space_size)
            if best and possible_space_size > best[1]:
                break
        else:
            reasonable_guess = sum(left) > 1 or left[-1] == 1
            max_left = max(left)
            if reasonable_guess and (not best or max_left < best[1]):
                best = (g, max_left)

    assert best
    return best[0]


def is_set[T](tpl: Permuation[T]) -> bool:
    return len(set(tpl)) == len(tpl)


def eval_hints[T](domain: list[T], guess: Permuation[T], solution: Permuation[T]):
    mask = [g == s for (g, s) in zip(guess, solution)]
    num_rplaces = sum(mask)

    counter_guess = {v: 0 for v in domain}
    counter_solution = {v: 0 for v in domain}
    for g, s, m in zip(guess, solution, mask):
        if not m:
            counter_guess[g] += 1
            counter_solution[s] += 1
    num_rvalues = sum(min(counter_guess[v], counter_solution[v]) for v in domain)

    return (num_rplaces, num_rvalues)


def compute_solution_space[T](
    domain: list[T], rep: int, allow_duplicates: bool
) -> SolutionSpace[T]:
    return [tpl for tpl in product(domain, repeat=rep) if (allow_duplicates or is_set(tpl))]


def compute_solutions[T](
    domain: list[T], solution_space: SolutionSpace[T], guesses: list[Guess[T]]
) -> SolutionSpace[T]:
    return [
        s for s in solution_space if all(eval_hints(domain, g, s) == (p, v) for g, p, v in guesses)
    ]


def main_print_solutions() -> None:
    combs = compute_solution_space(DOMAIN, IMAGE_SIZE, ALLOW_DUPLICATES)
    solutions = compute_solutions(DOMAIN, combs, GUESSES)

    print(f"Possible solutions: {len(solutions)}")
    for s in solutions:
        print(f"  {s}")


def main_interactive() -> None:
    solution_space = compute_solution_space(DOMAIN, IMAGE_SIZE, ALLOW_DUPLICATES)
    response_space = [
        (p, v) for p, v in product(range(IMAGE_SIZE + 1), repeat=2) if p + v <= IMAGE_SIZE
    ]

    while True:
        guess = compute_next_guess(DOMAIN, solution_space, response_space)
        print(guess)
        resp = input("Response: ")

        if not resp:
            break

        p, v = (int(x) for x in resp.split())
        GUESSES.append((guess, p, v))


if __name__ == "__main__":
    main_interactive()
    # main_print_solutions()
    # pass
