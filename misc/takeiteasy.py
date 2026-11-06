#!/usr/bin/env python3
"""Find high-scoring (and, by default, optimal) Take It Easy boards.

The 27 tiles are the cartesian product of three *indices*. Their printed values
depend on their axis: vertical uses 1/5/9, the main diagonal uses 2/6/7, and
the secondary diagonal uses 3/4/8. Completed lines are first found by index;
the score-optimal value permutation is assigned afterwards.
"""

from __future__ import annotations

from collections.abc import Sequence
from itertools import permutations, product
from pathlib import Path
from typing import TextIO

AXIS_NAMES = ("Vertical", "Main diagonal", "Secondary diagonal")
AXIS_VALUES = ((1, 5, 9), (2, 6, 7), (3, 4, 8))
INDICES = range(3)
RADIUS = 2


LinePattern = tuple[int | None, ...]


def make_cells() -> tuple[tuple[int, int, int], ...]:
    """Return axial board coordinates in a stable, printable order."""
    return tuple(
        (q, r, -q - r)
        for r in range(-RADIUS, RADIUS + 1)
        for q in range(-RADIUS, RADIUS + 1)
        if max(abs(q), abs(r), abs(q + r)) <= RADIUS
    )


CELLS = make_cells()
CELL_INDEX = {cell: index for index, cell in enumerate(CELLS)}
TILES = tuple(
    (first, second, third) for first in INDICES for second in INDICES for third in INDICES
)
TILE_OPTIONS = {
    requirement: tuple(
        tile_index
        for tile_index, tile in enumerate(TILES)
        if all(index is None or index == tile[axis] for axis, index in enumerate(requirement))
    )
    for requirement in product((*INDICES, None), repeat=3)
}


def line_lengths() -> tuple[int, ...]:
    return tuple(
        sum(cell[0] == coordinate for cell in CELLS) for coordinate in range(-RADIUS, RADIUS + 1)
    )


LINE_LENGTHS = line_lengths()


def best_value_assignment(
    axis: int, line_lengths_by_index: Sequence[int]
) -> tuple[int, tuple[int, int, int]]:
    """Assign an axis's printed values to indices for the greatest line score."""
    best_score = -1
    best_mapping = AXIS_VALUES[axis]
    for values in permutations(AXIS_VALUES[axis]):
        mapping = (values[0], values[1], values[2])
        score = sum(line_lengths_by_index[index] * mapping[index] for index in INDICES)
        if score > best_score:
            best_score, best_mapping = score, mapping
    return best_score, best_mapping


def best_value_assignments(
    axis: int, line_lengths_by_index: Sequence[int]
) -> tuple[tuple[int, int, int], ...]:
    """Return every value permutation that attains the best score for one axis."""
    best_score, _ = best_value_assignment(axis, line_lengths_by_index)
    return tuple(
        (values[0], values[1], values[2])
        for values in permutations(AXIS_VALUES[axis])
        if sum(line_lengths_by_index[index] * values[index] for index in INDICES) == best_score
    )


def is_canonical_index_pattern(indices: Sequence[int | None]) -> bool:
    """Keep one representative for the six interchangeable index permutations."""
    relabelled: dict[int, int] = {}
    for index in indices:
        if index is None:
            continue
        expected = relabelled.setdefault(index, len(relabelled))
        if index != expected:
            return False
    return True


def make_patterns() -> list[LinePattern]:
    """Generate canonical choices for the five parallel lines of one axis."""
    patterns: list[LinePattern] = []

    def build(indices: list[int | None]) -> None:
        if len(indices) == len(LINE_LENGTHS):
            if not is_canonical_index_pattern(indices):
                return
            patterns.append(tuple(indices))
            return
        for index in (*INDICES, None):
            indices.append(index)
            build(indices)
            indices.pop()

    build([])
    return patterns


def compatible_tiles(patterns: Sequence[LinePattern]) -> list[tuple[int, ...]]:
    """List tile indices that satisfy the selected line values for every cell."""
    options: list[tuple[int, ...]] = []
    for cell in CELLS:
        first, second, third = (
            pattern[coordinate + RADIUS]
            for pattern, coordinate in zip(patterns, cell, strict=True)
        )
        options.append(TILE_OPTIONS[(first, second, third)])
    return options


def has_repeated_fixed_tile(patterns: Sequence[LinePattern]) -> bool:
    """Reject the common high-score failure before running a full matching."""
    fixed_tiles: set[tuple[int, int, int]] = set()
    for cell in CELLS:
        first, second, third = (
            pattern[coordinate + RADIUS]
            for pattern, coordinate in zip(patterns, cell, strict=True)
        )
        if first is None or second is None or third is None:
            continue
        completed_tile = (first, second, third)
        if completed_tile in fixed_tiles:
            return True
        fixed_tiles.add(completed_tile)
    return False


def find_matching(options: Sequence[Sequence[int]]) -> list[int] | None:
    """Find distinct tiles for cells, if one exists (Kuhn augmenting paths)."""
    cell_order = sorted(range(len(CELLS)), key=lambda cell: len(options[cell]))

    # Most partial patterns are satisfiable without rearranging an earlier tile.
    unused_tiles = set(range(len(TILES)))
    greedy_assignment = [-1] * len(CELLS)
    for cell in cell_order:
        tile = next((tile for tile in options[cell] if tile in unused_tiles), None)
        if tile is None:
            break
        greedy_assignment[cell] = tile
        unused_tiles.remove(tile)
    else:
        return greedy_assignment

    tile_to_cell = [-1] * len(TILES)

    def augment(cell: int, seen: set[int]) -> bool:
        for tile in options[cell]:
            if tile in seen:
                continue
            seen.add(tile)
            previous = tile_to_cell[tile]
            if previous == -1 or augment(previous, seen):
                tile_to_cell[tile] = cell
                return True
        return False

    for cell in cell_order:
        if not augment(cell, set()):
            return None

    assignment = [-1] * len(CELLS)
    for tile, cell in enumerate(tile_to_cell):
        if cell != -1:
            assignment[cell] = tile
    return assignment


def completed_lengths_by_index(assignment: Sequence[int], axis: int) -> tuple[int, int, int]:
    """Sum the lengths of completed lines for each index in an axis."""
    lengths_by_index = [0, 0, 0]
    for coordinate, length in zip(range(-RADIUS, RADIUS + 1), LINE_LENGTHS, strict=True):
        tile_indices = [
            TILES[assignment[index]][axis]
            for index, cell in enumerate(CELLS)
            if cell[axis] == coordinate
        ]
        if len(set(tile_indices)) == 1:
            lengths_by_index[tile_indices[0]] += length
    return lengths_by_index[0], lengths_by_index[1], lengths_by_index[2]


def score_board(assignment: Sequence[int]) -> tuple[int, tuple[tuple[int, int, int], ...]]:
    """Score complete index lines with the best independent axis permutations."""
    mappings: list[tuple[int, int, int]] = []
    score = 0
    for axis in range(3):
        axis_score, mapping = best_value_assignment(
            axis, completed_lengths_by_index(assignment, axis)
        )
        score += axis_score
        mappings.append(mapping)
    return score, tuple(mappings)


def score_preserving_mappings(
    assignment: Sequence[int],
) -> tuple[tuple[tuple[int, int, int], ...], ...]:
    """Return every independent axis mapping that preserves this board's score."""
    return tuple(
        product(
            *(
                best_value_assignments(axis, completed_lengths_by_index(assignment, axis))
                for axis in range(3)
            )
        )
    )


def search(patterns: Sequence[LinePattern]) -> tuple[int, list[tuple[int, ...]], int]:
    """Exhaustively evaluate every canonical selection of three axis patterns."""
    best_score = -1
    best_assignments: set[tuple[int, ...]] = set()
    checks = 0

    for selected in product(patterns, repeat=3):
        checks += 1
        if not has_repeated_fixed_tile(selected):
            assignment = find_matching(compatible_tiles(selected))
            if assignment is not None:
                score, _ = score_board(assignment)
                if score > best_score:
                    best_score = score
                    best_assignments = {tuple(assignment)}
                elif score == best_score:
                    best_assignments.add(tuple(assignment))

    return best_score, sorted(best_assignments), checks


def line_indices(axis: int, coordinate: int, assignment: Sequence[int]) -> list[int]:
    """Return one scoring line's indices in a stable visual order."""
    cells = sorted(
        (cell for cell in CELLS if cell[axis] == coordinate),
        key=lambda cell: tuple(
            value for other_axis, value in enumerate(cell) if other_axis != axis
        ),
    )
    return [TILES[assignment[CELL_INDEX[cell]]][axis] for cell in cells]


def tile_art(values: Sequence[int]) -> tuple[str, str, str, str]:
    """Place the six endpoint values of one tile without drawing the lines."""
    vertical, main_diagonal, secondary_diagonal = values
    return (
        f"   {vertical}   ",
        f"{secondary_diagonal}     {main_diagonal}",
        f"{main_diagonal}     {secondary_diagonal}",
        f"   {vertical}   ",
    )


def print_tile_layout(
    assignment: Sequence[int], mappings: Sequence[Sequence[int]], output: TextIO
) -> None:
    """Draw a flat-top board where the vertical-axis values form screen columns."""
    tile_width = 7
    column_spacing = 12
    row_spacing = 6
    positions = {
        cell: (
            column_spacing * (cell[0] + RADIUS),
            -(row_spacing * cell[1] + 3 * cell[0]),
        )
        for cell in CELLS
    }
    minimum_y = min(y for _, y in positions.values())
    maximum_y = max(y for _, y in positions.values()) + 4
    width = column_spacing * (2 * RADIUS) + tile_width
    canvas = [[" "] * width for _ in range(maximum_y - minimum_y)]

    for cell, (x, y) in positions.items():
        tile = TILES[assignment[CELL_INDEX[cell]]]
        values = tuple(mappings[axis][index] for axis, index in enumerate(tile))
        for art_row, tile_row in enumerate(tile_art(values)):
            for offset, character in enumerate(tile_row):
                if character != " ":
                    canvas[y - minimum_y + art_row][x + offset] = character

    for canvas_row in canvas:
        print("".join(canvas_row).rstrip(), file=output)


def print_board(
    assignment: Sequence[int], mappings: Sequence[Sequence[int]], output: TextIO
) -> None:
    """Render tile values and all scoring lines so completed rows stand out."""
    print("Board layout (vertical-axis values run in screen columns):", file=output)
    print_tile_layout(assignment, mappings, output)

    print("\nScoring lines (* = completed):", file=output)
    for axis, name in enumerate(AXIS_NAMES):
        print(f"{name} ({'/'.join(map(str, AXIS_VALUES[axis]))}):", file=output)
        for coordinate, length in zip(range(-RADIUS, RADIUS + 1), LINE_LENGTHS, strict=True):
            indices = line_indices(axis, coordinate, assignment)
            values = [mappings[axis][index] for index in indices]
            completed = len(set(indices)) == 1
            suffix = f"* {length * values[0]:>2} points" if completed else ""
            print(
                f"  {' - '.join(f'{value:>2}' for value in values):<22} {suffix}",
                file=output,
            )


def write_solutions(score: int, assignments: Sequence[Sequence[int]]) -> list[Path]:
    """Write every maximum-scoring placement and value mapping to its own file."""
    output_directory = Path("_out/takeiteasy")
    output_directory.mkdir(parents=True, exist_ok=True)
    for old_file in output_directory.glob(f"{score}pts_*.txt"):
        old_file.unlink()

    files: list[Path] = []
    for assignment in assignments:
        for mappings in score_preserving_mappings(assignment):
            output_file = output_directory / f"{score}pts_{len(files) + 1}.txt"
            with output_file.open("w", encoding="ascii") as output:
                print(f"Score: {score} points", file=output)
                print_board(assignment, mappings, output)
            files.append(output_file)
    return files


def main() -> None:
    patterns = make_patterns()
    score, assignments, checks = search(patterns)
    total_selections = len(patterns) ** 3
    print(
        f"optimal score: {score} points after checking "
        f"{checks:,} of {total_selections:,} line selections"
    )
    files = write_solutions(score, assignments)
    print(f"Wrote {len(files)} solutions to _out/takeiteasy/")


if __name__ == "__main__":
    main()
