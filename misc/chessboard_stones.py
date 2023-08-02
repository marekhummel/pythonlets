# https://www.youtube.com/watch?v=m4Uth-EaTZ8


import sys
from typing import NamedTuple

Point = NamedTuple("Point", [("x", int), ("y", int)])
Bounds = NamedTuple("Bounds", [("xl", int), ("xh", int), ("yl", int), ("yh", int)])
Whites = dict[Point, int]
Result = NamedTuple("Result", [("nmax", int), ("whites", Whites), ("bounds", Bounds)])
Progress = NamedTuple("Progress", [("low", float), ("high", float)])


# Dont true both
PRINT_PROGRESS = False
PRINT_CURRENT_BEST = True

browns = [Point(0, 0), Point(2, 2)]
# browns = [Point(0, 0), Point(4, 2), Point(6, 4), Point(9, 2)]
# browns = [Point(0, 0), Point(3, 2), Point(2, -2), Point(5, -5), Point(8, -6), Point(11, -9)]  # takes long, 15min


def set_stone(n: int, bounds: Bounds, whites: Whites, progress: Progress) -> Result:
    best = None
    if PRINT_PROGRESS:
        sys.stdout.write(f"{progress.low * 100:.3f} %\r")

    possible = []
    for x in range(bounds.xl - 1, bounds.xh + 2):
        for y in range(bounds.yl - 1, bounds.yh + 2):
            pt = Point(x, y)

            # Cant stack stones
            if pt in whites or pt in browns:
                continue

            # Check value of this square
            total = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    dpt = Point(x + dx, y + dy)
                    if dpt in browns:
                        total += 1
                    elif dpt in whites:
                        total += whites[dpt]

            if total == n:
                possible.append(pt)

    if possible:
        progress_range = (progress.high - progress.low) / len(possible)
        for i, pt in enumerate(possible):
            # Set and continue with next stone
            new_whites = {**whites, pt: n}
            new_bounds = Bounds(min(bounds.xl, pt.x), max(bounds.xh, pt.x), min(bounds.yl, pt.y), max(bounds.yh, pt.y))
            result = set_stone(
                n + 1,
                new_bounds,
                new_whites,
                Progress(progress.low + i * progress_range, progress.low + (i + 1) * progress_range),
            )

            # Update best
            if best is None or result.nmax > best.nmax:
                if PRINT_CURRENT_BEST:
                    print_board(result.bounds, result.whites, True)
                best = result

    return best if best else Result(n - 1, whites, bounds)


def print_board(bounds: Bounds, whites: Whites, reset_cursor: bool):
    # Print board
    for y in range(bounds.yl - 1, bounds.yh + 2):
        for x in range(bounds.xl - 1, bounds.xh + 2):
            pt = Point(x, y)
            if pt in browns:
                sys.stdout.write(" BB ")
            elif pt in whites:
                n = whites[pt]
                sys.stdout.write(f" {n:02} ")
            else:
                sys.stdout.write("    ")

        print()

    # Reset cursor to top if wanted
    if reset_cursor:
        n_lines = bounds.yh - bounds.yl + 3
        print(f"\r\033[{n_lines}A", end="")


# Main
bounds_x = min(pt.x for pt in browns), max(pt.x for pt in browns)
bounds_y = min(pt.y for pt in browns), max(pt.y for pt in browns)
result = set_stone(2, Bounds(*bounds_x, *bounds_y), {}, Progress(0, 1))
n_max, whites, bounds = result
print_board(bounds, whites, False)
print(f"Max N: {n_max}")
