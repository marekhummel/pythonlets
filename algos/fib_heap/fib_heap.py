from typing import Self


class Node[T]:
    def __init__(self, value: tuple[int, T]) -> None:
        self.value: tuple[int, T] = value
        self.children: list[Node[T]] = []
        self.parent: Self | None = None
        self.marked = False

    def add_child(self, node: Self) -> None:
        self.children.append(node)
        node.parent = self

    def degree(self) -> int:
        return len(self.children)


class FiboMinHeap[T]:
    _rootlist: list[Node[T]]
    _node_lookup: dict[T, Node[T] | None]
    _front: int

    def __init__(self) -> None:
        self._rootlist = []
        self._node_lookup = {}
        self._front = -1

    def get_min(self) -> T | None:
        return self._rootlist[self._front].value[1] if self._front != -1 else None

    def extract_min(self) -> T | None:
        if self._front == -1:
            return None

        # Distribute children to root list (and remove min)
        min_root = self._rootlist.pop(self._front)
        for child in min_root.children:
            self._rootlist.append(child)
        min_root.children = []

        # Merge, so that each root has a different degree
        degree_map: list[Node[T] | None] = [None] * len(self._rootlist)
        for root in self._rootlist:
            deg = root.degree()

            merged = root
            while degree_map[deg] is not None:
                current = degree_map[deg]
                assert current
                merged = self._merge_nodes(current, merged)
                degree_map[deg] = None
                deg += 1

            degree_map[deg] = merged

        # Rebuild
        self._rootlist = []
        self._front = -1
        for new_root in degree_map:
            if new_root is None:
                continue
            self._extend_nodelist(new_root)

        # Get result (and remove lookup)
        elem = min_root.value[1]
        self._node_lookup[elem] = None
        return elem

    def insert(self, elem: T, prio: int) -> None:
        node = Node((prio, elem))
        if self._node_lookup.get(elem, None) is not None:
            raise ValueError("Element already existing")
        self._node_lookup[elem] = node
        self._extend_nodelist(node)

    def decrease_key(self, elem: T, new_prio: int) -> None:
        node = self._node_lookup[elem]
        if node is None:
            raise ValueError("Element not found")
        node.value = (new_prio, elem)

        cut_out = node
        while True:
            self._extend_nodelist(cut_out)
            cut_out.marked = False
            if not cut_out.parent:
                break

            parent = cut_out.parent
            parent.children.remove(cut_out)
            cut_out.parent = None
            if not parent.marked:
                parent.marked = True
                break

            cut_out = parent

    def _extend_nodelist(self, node: Node[T]) -> None:
        self._rootlist.append(node)
        if self._front == -1 or node.value[0] < self._rootlist[self._front].value[0]:
            self._front = len(self._rootlist) - 1

    def _merge_nodes(self, node1: Node[T], node2: Node[T]) -> Node[T]:
        if node1.value[0] > node2.value[0]:
            node1, node2 = node2, node1

        node1.add_child(node2)
        return node1


if __name__ == "__main__":
    h = FiboMinHeap[str]()
    prio = [1, 3, 4, 5, 4, 6, 6, 8, 5, 7]
    for i, p in enumerate(prio):
        h.insert(str(i), p)

    print("orig")
    print("insert")
    h.insert("x", 2)
    print("extract")
    print(h.extract_min())
    print("decrease")
    h.decrease_key("3", 1)
