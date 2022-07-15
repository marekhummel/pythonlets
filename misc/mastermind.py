from itertools import product



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
DOMAIN = ['red', 'green', 'white', 'blue', 'yellow', 'purple']

# Length of solution
IMAGE_SIZE = 3

# Can solution contain duplicate values ?
ALLOW_DUPLICATES = False

# Guesses done so far
GUESSES = []


# *********************

def compute_next_guess(solution_space, response_space):
    best = None
    for g in solution_space:
        left = []
        for p, v in response_space:
            guess = (g, p, v)
            guess_list = GUESSES + [guess]
            possible = compute_solutions(solution_space, guess_list)
            possible_space_size = len(possible)
            left.append(possible_space_size)
            if best and possible_space_size > best[1]:
                break
        else:
            reasonable_guess = sum(left) > 1 or left[-1] == 1
            max_left = max(left)
            if reasonable_guess and (not best or max_left < best[1]):
                best = (g, max_left)

    return best[0]


def is_set(tpl):
    return len(set(tpl)) == len(tpl)


def eval_hints(guess, solution):
    mask = [g == s for (g, s) in zip(guess, solution)]
    num_rplaces = sum(mask)

    counter_guess = {v: 0 for v in DOMAIN}
    counter_solution = {v: 0 for v in DOMAIN}
    for g, s, m in zip(guess, solution, mask):
        if not m:
            counter_guess[g] += 1
            counter_solution[s] += 1
    num_rvalues = sum(min(counter_guess[v], counter_solution[v]) for v in DOMAIN)

    return (num_rplaces, num_rvalues)


def compute_solution_space():
    return [tpl for tpl in product(DOMAIN, repeat=IMAGE_SIZE) if (ALLOW_DUPLICATES or is_set(tpl))]


def compute_solutions(solution_space, guesses):
    return [s for s in solution_space if all(eval_hints(g, s) == (p, v) for g, p, v in guesses)]


def main_print_solutions():
    combs = compute_solution_space()
    solutions = compute_solutions(combs, GUESSES)

    print(f'Possible solutions: {len(solutions)}')
    for s in solutions:
        print(f'  {s}')


def main_iterative():
    solution_space = compute_solution_space()
    response_space = [(p, v) for p, v in product(range(IMAGE_SIZE + 1), repeat=2) if p + v <= IMAGE_SIZE]

    while True:
        guess = compute_next_guess(solution_space, response_space)
        print(guess)
        resp = input('Response: ')

        if not resp:
            break

        p, v = [int(x) for x in resp.split()]
        GUESSES.append((guess, p, v))


if __name__ == '__main__':
    main_iterative()
    # main_print_solutions()
    # pass
