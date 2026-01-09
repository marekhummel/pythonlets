from itertools import combinations as comb

from cell import Cell


class Sudoku:
    def __init__(self):
        self.cells = [[Cell(r, c) for c in range(9)] for r in range(9)]

    # Screen output
    def print_to_screen(self):
        print()

        for ri, row in enumerate(self.cells):
            for ci, cell in enumerate(row):
                print(" " + str(cell), end="")
                if ci % 3 == 2 and ci != 8:
                    print(" |", end="")
            print()
            if ri % 3 == 2 and ri != 8:
                print("-------+-------+-------")

        print()

    # Updating cell by adding the number and removing it
    # as a candidate in all adjacent cells
    def update_cell(self, r, c, val):
        for cell in self.get_cells_in_row(r):
            cell.remove_candidate(val)
        for cell in self.get_cells_in_column(c):
            cell.remove_candidate(val)
        for cell in self.get_cells_in_box(r, c):
            cell.remove_candidate(val)

        self.cells[r][c].set_value(val)

    # Returns number of missing cells
    def missing_cells(self):
        return len([c for c in sum(self.cells, []) if c.value == 0])

    # -- Returns generator of cells of a certain line / box --

    def get_cells_in_row(self, r):
        for c in range(9):
            yield self.cells[r][c]

    def get_cells_in_column(self, c):
        for r in range(9):
            yield self.cells[r][c]

    def get_cells_in_box(self, r, c):
        top, left = r // 3 * 3, c // 3 * 3
        for r in range(top, top + 3):
            for c in range(left, left + 3):
                yield self.cells[r][c]

    # -- Returns generator of all rows / columns / boxes --

    def get_all_rows(self):
        for r in range(9):
            yield self.get_cells_in_row(r)

    def get_all_columns(self):
        for c in range(9):
            yield self.get_cells_in_column(c)

    def get_all_boxes(self):
        for r in range(0, 9, 3):
            for c in range(0, 9, 3):
                yield self.get_cells_in_box(r, c)

    # -- Returns list of all rows, columns and boxes --

    def get_all_groups(self):
        return (
            list(self.get_all_rows()) + list(self.get_all_columns()) + list(self.get_all_boxes())
        )

    # Read from string
    def read(self, s):
        assert len(s) == 81
        nums = s.replace(".", "0")
        for i in range(len(nums)):
            c, r = i % 9, i // 9
            if nums[i] != "0":
                self.update_cell(r, c, int(nums[i]))

    # Checks if the sudoku is solvable
    def is_valid(self):
        return all(
            not (cell.value == 0 and len(cell.candidates) == 0) for cell in sum(self.cells, [])
        )

    # Clone
    def clone(self):
        clone = Sudoku()
        for c in sum(self.cells, []):
            nc = Cell(c.row, c.column)
            if c.value != 0:
                nc.set_value(c.value)
            else:
                nc.candidates = c.candidates.copy()
            clone.cells[c.row][c.column] = nc

        return clone

    # Overrides self with a different sudoku
    def override(self, other):
        for c in sum(other.cells, []):
            nc = Cell(c.row, c.column)
            if c.value != 0:
                nc.set_value(c.value)
            else:
                nc.candidates = c.candidates.copy()
            self.cells[c.row][c.column] = nc

    # ===== SOLVE =====

    # Only one possible candidate left in any cell
    def naked_single(self):
        for cell in sum(self.cells, []):
            if cell.value != 0:
                continue
            if len(cell.candidates) == 1:
                self.update_cell(cell.row, cell.column, list(cell.candidates)[0])

    # One number only possible in one cell of any row/column/box
    def hidden_single(self):
        for group in self.get_all_groups():
            for n in range(1, 10):
                possible = [cell for cell in group if cell.value == 0 and n in cell.candidates]
                if len(possible) == 1:
                    cell = possible[0]
                    self.update_cell(cell.row, cell.column, n)

    # If the cells of one candidate happen to be in the same line and box,
    # the candidate can be removed in every other cell in the box and line
    # //checked by boxes, removes in lines only
    def box_line_interaction(self):
        for box in [list(b) for b in self.get_all_boxes()]:
            for n in (n for n in range(1, 10)):
                # Cells where n is still possible
                cells = [c for c in box if c.value == 0 and n in c.candidates]

                # Continue if not 2 or 3 cells (makes no sense)
                if not (2 <= len(cells) <= 3):
                    continue

                # All same row
                if all(c.row == cells[0].row for c in cells):
                    row = self.get_cells_in_row(cells[0].row)
                    row = [c for c in row if c not in cells]
                    for c in row:
                        c.remove_candidate(n)

                # All same column
                elif all(c.column == cells[0].column for c in cells):
                    column = self.get_cells_in_column(cells[0].column)
                    column = [c for c in column if c not in cells]
                    for c in column:
                        c.remove_candidate(n)

    # If the cells of one candidate happen to be in the same line and box,
    # the candidate can be removed in every other cell in the box and line
    # //checked by lines, removes in boxes only
    def line_box_interaction(self):
        lines = [list(ln) for ln in (list(self.get_all_columns()) + list(self.get_all_rows()))]
        for line in lines:
            for n in (n for n in range(1, 10)):
                # Cells where n is still possible
                cells = [c for c in line if c.value == 0 and n in c.candidates]

                # Continue if not 2 or 3 cells (makes no sense)
                if not (2 <= len(cells) <= 3):
                    continue

                # All same box
                if all(c.get_box_index() == cells[0].get_box_index() for c in cells):
                    box = self.get_cells_in_box(cells[0].row, cells[0].column)
                    box = [c for c in box if c not in cells]
                    for c in box:
                        c.remove_candidate(n)

    # Naked tuples (pairs, triples, quads) are a set of 2/3/4 candidates blocking 2/3/4 cells by
    # being the only possible candidates in these cells
    # Being in the same grp, although its unknown which belongs to which cell, it can be said
    # for sure, that the candidates can be cancelled in every other cell in the same grp.
    def naked_tuple(self, n):
        assert 2 <= n <= 4

        # Iterate over all grps
        for group in self.get_all_groups():
            group = set(group)
            # Only take cells with n or less candidates, and continue if less than n cells
            selected = [c for c in group if 2 <= len(c.candidates) <= n]
            if len(selected) < n:
                continue

            # Iterate over all subsets of these
            for subset in comb(selected, n):
                subset = set(subset)
                all_marks = set().union(*[c.candidates for c in subset])

                if len(all_marks) == n:
                    # Naked tuple found
                    for cell in group - subset:
                        for mark in all_marks:
                            cell.remove_candidate(mark)

    # ===== MAINS =====

    def solve(self):
        # Logic attempt first
        if self.solve_human():
            return True
        if not self.is_valid():
            return False

        # - Brute force now -
        firstmissing = next(c for c in sum(self.cells, []) if c.value == 0)

        # Try each candidate
        for can in firstmissing.candidates:
            copy = self.clone()
            copy.update_cell(firstmissing.row, firstmissing.column, can)

            if copy.solve():
                self.override(copy)
                return True

            del copy

        # Sudoku not solvable
        return False

    # Solves sudoku with pure logic
    def solve_human(self):
        while True:
            miss = self.missing_cells()

            self.naked_single()
            self.hidden_single()
            self.box_line_interaction()
            self.line_box_interaction()
            for n in range(2, 5):
                self.naked_tuple(n)

            if self.missing_cells() == miss or not self.is_valid():
                break

        return self.missing_cells() == 0
