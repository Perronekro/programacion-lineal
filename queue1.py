# ─────────────────────────────────────────────────────────────
# Node for Linked List
# ─────────────────────────────────────────────────────────────
class Node:
    """Single node used in the linked list implementation."""
    
    def __init__(self, data):
        self.data = data
        self.next = None


# ─────────────────────────────────────────────────────────────
# Queue implemented using a Linked List
# FIFO: First In, First Out
# ─────────────────────────────────────────────────────────────
class Queue:

    def __init__(self, initial_elements=None):
        """
        Initialize the queue.
        Optionally accepts an iterable of initial elements.
        """
        self.head = None      # Front of queue (next element to pop)
        self.tail = None      # Back of queue (last pushed element)
        self._length = 0

        if initial_elements:
            for element in initial_elements:
                self.push(element)

    # ─────────────────────────────────────────────────────────
    # String representation
    # ─────────────────────────────────────────────────────────
    def __str__(self):
        elements = []
        current = self.head

        while current:
            elements.append(str(current.data))
            current = current.next

        return f"FRONT → [{' | '.join(elements)}] ← BACK"

    # ─────────────────────────────────────────────────────────
    # Basic utilities
    # ─────────────────────────────────────────────────────────
    def __len__(self):
        return self._length

    def is_empty(self):
        return self._length == 0

    def peek(self):
        """Return the element at the front without removing it."""
        if self.is_empty():
            raise IndexError("Peek from empty queue")

        return self.head.data

    # ─────────────────────────────────────────────────────────
    # Iteration support
    # ─────────────────────────────────────────────────────────
    def __iter__(self):
        current = self.head

        while current:
            yield current.data
            current = current.next

    def __contains__(self, value):
        for item in self:
            if item == value:
                return True
        return False

    # ─────────────────────────────────────────────────────────
    # Core queue operations
    # ─────────────────────────────────────────────────────────
    def push(self, value):
        """
        Enqueue operation.
        Adds an element to the back of the queue.
        """
        new_node = Node(value)

        if self.tail is None:   # Queue is empty
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        self._length += 1

    def pop(self):
        """
        Dequeue operation.
        Removes and returns the element at the front (FIFO).
        """
        if self.is_empty():
            raise IndexError("Pop from empty queue")

        value = self.head.data
        self.head = self.head.next

        if self.head is None:   # Queue became empty
            self.tail = None

        self._length -= 1
        return value


# ─────────────────────────────────────────────────────────────
# Demo
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":

    q = Queue([1, 2, 3])

    print("Initial queue:")
    print(q)

    print("\nQueue length:", len(q))
    print("Is empty?:", q.is_empty())
    print("Front element (peek):", q.peek())

    print("\nContains 2?", 2 in q)
    print("Contains 99?", 99 in q)

    print("\nAdding elements (push):")
    q.push(4)
    q.push(5)
    print(q)

    print("\nRemoving elements (pop):")
    print("Popped:", q.pop())
    print(q)

    print("Popped:", q.pop())
    print(q)

    print("\nIterating through queue:")
    for element in q:
        print(element)