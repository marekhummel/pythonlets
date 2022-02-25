class Cell:
    ''' A cell defines itself over an index
        (row and column plus a value or a set of candidates) '''

    def __init__(self, r, c):
        self.row = r
        self.column = c
        self.value = 0
        self.candidates = set((1, 2, 3, 4, 5, 6, 7, 8, 9))

    def set_value(self, v):
        self.value = v
        self.candidates = set()

    def remove_candidate(self, c):
        if (c in self.candidates):
            self.candidates.remove(c)

    # Returns the index of the box the cell is in, 0 to 8, left to right, top to bottom
    def get_box_index(self):
        return self.row // 3 * 3 + self.column // 3

    def __str__(self):
        return " " if self.value == 0 else str(self.value)

    def __repr__(self):
        return "Cell(%r|%r => %r)" % (self.row, self.column, self.value if self.value != 0 else self.candidates)