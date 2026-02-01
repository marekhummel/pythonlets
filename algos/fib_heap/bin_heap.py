class BinaryMinHeap[T]:
    _data: list[tuple[int, T]]

    def __init__(self) -> None:
        self._data = []

    def get_min(self) -> T:
        return self._data[0][1]

    def extract_min(self) -> T:
        self._swap(0, len(self._data) - 1)
        result = self._data.pop()

        current = 0
        while True:
            left, right = self._get_children(current)

            if left >= len(self._data):
                break

            lower = (
                left
                if right >= len(self._data) or self._data[left][0] <= self._data[right][0]
                else right
            )

            if self._data[lower][0] < self._data[current][0]:
                self._swap(lower, current)
            current = lower

        return result[1]

    def insert(self, elem: T, prio: int) -> None:
        self._data.append((prio, elem))
        self._heapify(len(self._data) - 1)

    def decrease_key(self, elem: T, new_prio: int):
        for index, val in enumerate(self._data):
            if val[1] == elem:
                break
        else:
            return

        self._data[index] = (new_prio, self._data[index][1])
        self._heapify(index)

    def _get_parent(self, index: int) -> int:
        return (index - 1) // 2

    def _get_children(self, index: int) -> tuple[int, int]:
        return index * 2 + 1, index * 2 + 2

    def _swap(self, a: int, b: int) -> None:
        self._data[a], self._data[b] = self._data[b], self._data[a]

    def _heapify(self, start: int) -> None:
        current = start
        while True:
            parent = self._get_parent(current)

            if parent < 0:
                break

            if self._data[parent][0] < self._data[current][0]:
                break

            self._swap(parent, current)
            current = parent


if __name__ == "__main__":
    h = BinaryMinHeap[str]()
    prio = [1, 3, 4, 5, 4, 6, 6, 8, 5, 7]
    h._data = [(p, str(i)) for i, p in enumerate(prio)]

    print("orig")
    print(h._data)
    print("insert")
    h.insert("x", 2)
    print(h._data)
    print("extract")
    print(h.extract_min())
    print(h._data)
    print("decrease")
    h.decrease_key("3", 1)
    print(h._data)
