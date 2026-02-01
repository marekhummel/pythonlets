from typing import Protocol

from bin_heap import BinaryMinHeap
from fib_heap import FiboMinHeap


class PriorityQueueProtocol[T](Protocol):
    def enqueue(self, elem: T, prio: int) -> None: ...
    def dequeue(self) -> T | None: ...
    def update(self, elem: T, new_prio: int) -> None: ...


class PriorityQueueBinHeap[T]:
    """
    PQ with heap as backend, yields peek in constant time and
    enqueue / dequeue / update in logarithmic time
    """

    _data: BinaryMinHeap[T]

    def __init__(self) -> None:
        self._data = BinaryMinHeap()

    def empty(self) -> bool:
        return len(self._data._data) == 0

    def front(self) -> T:
        return self._data.get_min()

    def update(self, elem: T, new_prio: int) -> None:
        self._data.decrease_key(elem, new_prio)

    def dequeue(self) -> T | None:
        return self._data.extract_min()

    def enqueue(self, elem: T, prio: int) -> None:
        self._data.insert(elem, prio)


class PriorityQueueFiboHeap[T]:
    """
    PQ with heap as backend, yields peek in constant time,
    enqueue and update in  constant time as well and only dequeue
    in logarithmic time (plus constant compared to bin heap)
    """

    _data: FiboMinHeap[T]

    def __init__(self) -> None:
        self._data = FiboMinHeap()

    def empty(self) -> bool:
        return len(self._data._rootlist) == 0

    def front(self) -> T | None:
        return self._data.get_min()

    def update(self, elem: T, new_prio: int) -> None:
        self._data.decrease_key(elem, new_prio)

    def dequeue(self) -> T | None:
        return self._data.extract_min()

    def enqueue(self, elem: T, prio: int) -> None:
        self._data.insert(elem, prio)


class PriorityQueueNaive[T]:
    """
    PQ with simple list as PQ, yields peek in constant time, enqueue and
    update in constant time as well, but dequeue in linear time
    """

    _data: list[tuple[int, T]]
    _front: int

    def __init__(self) -> None:
        self._data = []
        self._front = -1

    def empty(self) -> bool:
        return len(self._data) == 0

    def front(self) -> T | None:
        return self._data[self._front][1] if self._front != -1 else None

    def update(self, elem: T, new_prio: int) -> None:
        for index, val in enumerate(self._data):
            if val[1] == elem:
                break
        else:
            return

        self._data[index] = (new_prio, self._data[index][1])
        if new_prio < self._data[self._front][0]:
            self._front = index

    def dequeue(self) -> T | None:
        if self._front == -1:
            return None

        result = self._data.pop(self._front)[1]
        front = 0
        for i, v in enumerate(self._data):
            if v[0] < self._data[front][0]:
                front = i
        self._front = front
        return result

    def enqueue(self, elem: T, prio: int) -> None:
        self._data.append((prio, elem))
        if self._front == -1 or self._data[self._front][0] > prio:
            self._front = len(self._data) - 1
