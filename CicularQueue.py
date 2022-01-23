

class CircularQueue:

    # ---------------------- internal Node class ------------------------
    class _Node:
        __slots__ = 'elem', 'next'

        def __init__(self, e, next):
            self.elem = e
            self.next = next

    # -------------------- internal queue methods -----------------------
    __slots__ = '_size', '_tail'

    def __init__(self):
        self._size = 0
        self._tail = None

    def __len__(self):
        """Returns the number of elements in the queue"""
        return self._size

    def is_empty(self):
        """Returns true if queue is empty"""
        return self._size == 0

    def peek(self):
        """Returns the element in front of the queue"""
        if self.is_empty():
            raise Exception('queue is empty')
        first = self._tail.next
        return first.elem

    def enqueue(self, elem):
        """Pushes the element to end of the queue"""
        if self.is_empty():
            self._tail = self._Node(elem, None)
            self._tail.next = self._tail
        else:
            self._tail.next = self._Node(elem, self._tail.next)
            self._tail = self._tail.next
        self._size += 1

    def dequeue(self):
        """Removes and returns the element in front of the queue"""
        if self.is_empty():
            raise Exception('queue is empty')
        first = self._tail.next
        self._tail.next = first.next
        self._size -= 1
        return first.elem


# if __name__ == '__main__':
#     mu_queue = CircularQueue()
#     mu_queue.enqueue(1)
#     mu_queue.enqueue(2)
#     mu_queue.enqueue(3)
#     mu_queue.enqueue(4)
#     print(mu_queue.peek())
#     print(mu_queue.dequeue())
#     print(mu_queue.peek())
#     print(mu_queue.dequeue())
#     print(mu_queue.peek())
#     print(mu_queue.dequeue())
