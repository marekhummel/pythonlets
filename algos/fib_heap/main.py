# Fibonacci Heaps
# https://www.youtube.com/watch?v=6JxvKfSV9Ns

from prio_queue import PriorityQueueBinHeap, PriorityQueueFiboHeap, PriorityQueueNaive

pqh = PriorityQueueBinHeap()
pqn = PriorityQueueNaive()
pqf = PriorityQueueFiboHeap()

for pq in [pqh, pqn, pqf]:
    pq.enqueue("x", 1)
    pq.enqueue("b", 5)
    pq.enqueue("a", 7)
    pq.enqueue("z", 2)
    pq.enqueue("c", 6)
    print(pq.dequeue())
    print(pq.dequeue())
    pq.enqueue("y", 1)
    print(pq.dequeue())
    pq.update("a", 4)
    print(pq.dequeue())
    print(pq.dequeue())
    print(pq.dequeue())
    print("----")
