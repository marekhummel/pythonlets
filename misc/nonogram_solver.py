from datetime import datetime

NONE, BOX, SPACE = "?", "\u25fc", "\u00b7"


def solve(nonogram):
    """Solves the nonogram"""
    row_clues, col_clues = nonogram
    row_count, col_count = len(row_clues), len(col_clues)

    # Init grid
    grid = [[NONE] * col_count for _ in range(row_count)]

    # Try solving while changes are made
    last_changed = ([True] * row_count, [True] * col_count)
    while True:
        changed = ([False] * row_count, [False] * col_count)
        for row in range(row_count):
            if last_changed[0][row]:
                prefixed = grid[row]
                line = find_fixed(row_clues[row], prefixed)
                for i in range(len(line)):
                    if line[i] != NONE and grid[row][i] == NONE:
                        changed[0][row] = True
                        changed[1][i] = True
                        grid[row][i] = line[i]

        for col in range(col_count):
            if last_changed[1][col]:
                prefixed = [grid[i][col] for i in range(row_count)]
                line = find_fixed(col_clues[col], prefixed)
                for i in range(len(line)):
                    if line[i] != NONE and grid[i][col] == NONE:
                        changed[0][i] = True
                        changed[1][col] = True
                        grid[i][col] = line[i]

        # No new information, abort
        if not any(changed[0]) and not any(changed[1]):
            break
        last_changed = changed

    return grid


def find_fixed(clues, prefixed):
    """Finds fixed solutions in line"""
    # Get all possible solutions and filter with already set cells
    possibles = list(enumerate_line(clues, prefixed))
    assert len(possibles) > 0

    # Only one possible solution
    if len(possibles) == 1:
        return possibles[0]

    # Set cells which are equal among all possibles
    line = [NONE] * len(prefixed)
    for i in range(len(prefixed)):
        entry = [p[i] for p in possibles]
        if entry.count(entry[0]) == len(entry):
            line[i] = possibles[0][i]
    return line


def enumerate_line(clues, fixed):
    """Creates all possible fillings of this line"""
    # Min length of line given the clues
    length = len(fixed)
    min_length = sum(clues) + len(clues) - 1
    assert min_length <= length

    # Try each position for the first block
    n = clues[0]
    for i in range(length - min_length + 1):
        rem_len = length - n - i

        # Set block and check if it still matches the fixed ones
        line = [SPACE] * i + [BOX] * n + [NONE] * rem_len
        if rem_len > 0:
            line[n + i] = SPACE
        if not match_state(fixed[: n + i + 1], line[: n + i + 1]):
            continue

        if len(clues) > 1:
            # More than one block left, append x and find possibles for rest
            for e in enumerate_line(clues[1:], fixed[n + i + 1 :]):
                result = line[: -len(e)] + e
                if match_state(fixed, result):
                    yield result
        else:
            # Last block was be set, rest is x
            result = line[: n + i + 1] + [SPACE] * (rem_len - 1)
            if match_state(fixed, result):
                yield result


def match_state(fixed, possible):
    return all(fixed[i] in [NONE, possible[i]] for i in range(len(fixed)))


def print_grid(grid):
    """Displays grid"""
    for row in grid:
        for cell in row:
            print(cell, end=" ")
        print()


def letter_conv(s):
    return [[ord(letter) - ord("A") + 1 for letter in word] for word in s.split()]


# rows = [[1, 3], [3], [4], [1], [1]]
# cols = [[1], [2], [4], [3], [1, 1, 1]]

# rows = [[12,35,19],[1,18,17],[1,20,20,13],[4,22,22],[1,5,23,23,9],[2,24,24],[4,25,25],[2,4,25,25],[3,26,26],[2,2,26,26],[4,2,26,26],[5,1,2,26,26],[1,1,2,1,26,26],[1,1,1,5,11,14,11,5],[1,1,2,2,6,5,2,5,6,3,2],[1,1,1,6,2,7,9],[1,2,26],[2,24,1],[4,6,2,11,3,6],[8,2,2,2,9,2,5],[10,3,3,2,2,6,4],[4,7,13,5,6,2,5,2,2,5],[2,2,4,2,1,6,1,2,6,4,6,5],[7,8,4,1,1,3,1,4,1,2,6,2,2,2,5],[6,2,2,4,5,1,4,1,2,7,1,1,1,5],[2,2,6,2,4,1,1,3,2,1,6,1,2,7,1,1,1,6],[5,2,2,3,2,3,3,4,5,5,2,4,2,2,2,3],[1,1,1,4,2,4,6,3,3,2,4,2,2,1,4],[3,2,1,1,4,1,14,2,2,2,3,2,2,1,1,4],[2,3,4,1,4,5,2,6,2,3,1,1,4],[1,5,9,5,5,2,2,3,4,4],[1,6,1,4,2,4,1,3,1,4,2,3,1,1,3],[1,4,2,3,2,1,1,1,3,2,1,2,4,13,4],[2,4,1,1,1,1,1,4,2,7,3,3,2,2],[3,6,1,1,4,3,2,3,2,2,2,1,12,2],[2,2,2,2,1,11,2,2,2,2,2,10,1,3,3],[2,2,2,2,2,2,10,2,2,5,1,2,8,1,1,1,1,1],[2,9,1,1,2,1,1,5,2,6,1,6,2,1,1,1,1],[1,10,2,2,2,1,2,2,2,2,1,1,2,2,1],[1,10,1,2,3,2,1,1,2,2,1,1,1,1],[2,9,1,2,1,1,2,1,7,3,3,2,1,1,2],[4,12,1,1,2,1,1,1,3,5,1,3,4],[2,8,1,10,1,1,1,8,2,1,1,1,3],[2,8,2,7,2,2,6,3,6,1,1,2,1],[3,8,8,1,1,7,9,4,2],[3,10,1,2,2,2,8,7,3,1,1,1],[4,18,3,14,13,7,2,2,2,2],[7,12,1,1,2,2,2,3,7,6,2,7,2],[20,6,4,13,2,8,8,2,1,2,1],[20,1,1,2,1,1,2,23,2,2,1],[4,2,3,7,5,11,2,21,2,2,2],[1,1,1,1,1,1,2,1,2,21,3,1,2],[1,1,1,1,1,1,1,1,2,19,3,1,2],[6,1,14,6,11,2,19,6,2],[6,1,14,6,10,3,3,19,2,3],[6,1,15,6,9,1,1,1,1,19,1,2],[6,2,15,6,9,1,1,1,1,19,1,1,3],[6,1,15,6,9,1,2,2,1,19,1,1,2],[6,1,15,6,8,1,3,1,19,2,1,2],[5,1,15,7,8,3,2,19,1,1,2],[1,1,1,1,1,1,2,1,10,19,1,1,2],[1,1,1,2,1,1,2,1,2,1,19,2,1,1],[1,1,1,1,2,1,2,1,1,2,19,2,1,1],[1,1,1,1,2,3,2,1,4,21,2,1,1],[1,1,2,1,2,9,30,3,1,2],[1,1,4,3,3,8,2,33,2],[1,2,3,10,14,30,3,3],[2,12,11,6,30,2,4],[2,13,11,6,30,2,5],[22,21,30,8]]  # noqa
# cols = [[6,1,2,1,4,7],[1,1,2,1,2,2,3,7],[1,1,2,1,5,2,1,5,7],[1,1,2,1,2,3,1,7,7],[6,6,2,1,10,16],[1,3,1,5,1,17,3],[2,2,2,4,3,3,1],[5,2,2,5,4,3,1],[1,3,1,2,4,9,2,1],[3,1,1,2,6,9,5,11,1],[3,2,1,1,2,1,7,5,3,2,1],[7,2,1,1,1,1,2,1,17,1,1],[1,1,1,2,1,1,1,1,1,1,14,3],[1,1,2,3,1,1,1,18,10,3],[1,2,1,2,2,3,1,15,7,2,3],[1,1,1,2,1,8,21,1,3],[1,1,1,2,2,10,10,7,1,3],[1,1,3,2,6,2,1,8,7,5],[1,1,4,2,4,3,1,6,7,4],[1,5,2,1,4,4,7,4],[1,5,3,4,7,3],[1,5,3,1,1,7,3],[1,6,2,2,1,1,1,7,2],[7,1,2,1,1,1,7,2],[7,3,2,1,4,1,1,1,7,2],[8,8,2,3,2,1,1,1,7,1],[8,12,2,2,3,1,1,7,1],[9,12,1,1,4,15],[9,5,5,7,3,6],[10,4,1,2,9,3,3],[11,4,1,1,2,3,3,10,3],[11,4,1,2,1,2,3,1,18,2,3],[12,3,3,2,5,1,1,7,2,3],[12,12,3,3,2,3,1,7,6],[12,24,4,7,5],[14,2,8,3,2,11,5],[14,1,1,7,3,2,5,4],[15,1,2,2,4,2,3,1,4],[15,1,2,4,1,4,10,2,3],[15,1,2,1,6,9,1,3],[16,6,2,2,1,1,1,7,2,2,2],[13,1,2,2,3,2,1,1,1,7,5,2],[12,1,3,3,1,2,1,1,1,7,4,1],[11,1,5,5,1,1,1,1,1,7,3,1],[10,1,1,6,1,1,1,1,1,1,7,4,1],[9,2,1,4,1,1,1,1,1,1,15,1],[8,1,1,5,1,3,1,1,1,5,6],[7,1,1,6,1,1,1,1,2,5],[6,1,5,5,1,1,4,4],[5,2,3,3,7,1,3,4],[4,1,2,2,4,6,1,2],[3,1,6,3,3,2,1,2],[2,1,2,2,1,1],[1,1,1,1,2,1,1],[1,1,1,1,7,2],[1,25,1,9,2,2],[1,25,1,1,12,1,2],[1,1,1,2,1,1,2,2,1,3],[1,1,2,1,1,1,1,1,10],[2,1,1,7,2,1,1,1,2,2,1,7],[3,1,3,9,4,1,4,4,1,6],[4,1,3,11,9,1,2,6],[5,2,12,3,6,6,6],[6,12,2,8,7],[7,15,6,27],[8,15,4,27],[9,9,32],[10,6,2,2,2,24],[11,5,2,3,2,23],[12,4,1,4,1,22],[13,3,2,1,1,3,2,21],[15,2,2,1,4,1,21],[14,2,3,1,4,1,21],[14,2,1,1,1,4,1,21],[14,2,6,1,1,4,1,21],[14,3,2,5,1,4,1,21],[13,3,2,1,4,1,21],[12,5,2,1,1,3,2,22],[12,3,1,1,4,1,22],[12,3,2,3,2,24],[11,4,2,31],[1,11,4,33],[1,10,8,4,5,27],[1,9,13,4,9,7],[1,9,12,1,7,3,6],[1,8,2,15,4,4,5],[1,8,1,1,12,2,9],[1,1,7,2,10,6,1,6,8],[1,1,7,4,1,13,2],[1,1,6,4,1,3,2],[1,1,5,4,2,2,16],[1,1,1,5,4,1,2,3],[1,1,1,5,4,1,2,1,1,2],[1,1,1,4,4,5,2,1,1],[1,1,1,3,1,4,1,4,1],[1,1,1,2,7,2,1,2],[1,1,1,2,1,5,4,3],[1,1,1,1,4,1,7,4],[1,1,1,1,2,3,5,6],[1,1,1,1,7,11]]  # noqa

rows = "D A CC E D D C AC AC AAD BBB D"
cols = "A AA AA CD BB DAA FB CE CB BB BB"


nonogram = (letter_conv(rows), letter_conv(cols))
start = datetime.now()
print_grid(solve(nonogram))
print(datetime.now() - start)
