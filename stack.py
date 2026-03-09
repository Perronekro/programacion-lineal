# ─────────────────────────────────────────────────────────────
# Node for Linked List
# ─────────────────────────────────────────────────────────────
class Node:
    """Single node used in the linked list implementation."""

    def __init__(self, data):
        self.data = data
        self.next = None


# ─────────────────────────────────────────────────────────────
# Stack implemented using a Linked List
# LIFO: Last In, First Out
# ─────────────────────────────────────────────────────────────
class Stack:

    def __init__(self, initial_elements=None):
        """
        Initialize the stack.
        Optionally accepts an iterable of initial elements.
        """
        self.top = None
        self._length = 0

        if initial_elements:
            for element in initial_elements:
                self.push(element)

    # ─────────────────────────────────────────────────────────
    # String representation
    # ─────────────────────────────────────────────────────────
    def __str__(self):
        elements = []
        current = self.top

        while current:
            elements.append(str(current.data))
            current = current.next

        return f"TOP → [{' | '.join(elements)}]"

    # ─────────────────────────────────────────────────────────
    # Basic utilities
    # ─────────────────────────────────────────────────────────
    def __len__(self):
        return self._length

    def is_empty(self):
        return self._length == 0

    def peek(self):
        """Return the top element without removing it."""
        if self.is_empty():
            raise IndexError("Peek from empty stack")

        return self.top.data

    # ─────────────────────────────────────────────────────────
    # Iteration support
    # ─────────────────────────────────────────────────────────
    def __iter__(self):
        current = self.top

        while current:
            yield current.data
            current = current.next

    def __contains__(self, value):
        for item in self:
            if item == value:
                return True
        return False

    # ─────────────────────────────────────────────────────────
    # Core stack operations
    # ─────────────────────────────────────────────────────────
    def push(self, value):
        """
        Push operation.
        Adds an element to the top of the stack.
        """
        new_node = Node(value)
        new_node.next = self.top
        self.top = new_node

        self._length += 1

    def pop(self):
        """
        Pop operation.
        Removes and returns the element at the top (LIFO).
        """
        if self.is_empty():
            raise IndexError("Pop from empty stack")

        value = self.top.data
        self.top = self.top.next

        self._length -= 1
        return value


# ─────────────────────────────────────────────────────────────
# Demo
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":

    s = Stack([1, 2, 3])

    print("Initial stack:")
    print(s)

    print("\nStack length:", len(s))
    print("Is empty?:", s.is_empty())
    print("Top element (peek):", s.peek())

    print("\nContains 2?", 2 in s)
    print("Contains 99?", 99 in s)

    print("\nAdding elements (push):")
    s.push(4)
    s.push(5)
    print(s)

    print("\nRemoving elements (pop):")
    print("Popped:", s.pop())
    print(s)

    print("Popped:", s.pop())
    print(s)

    print("\nIterating through stack (top → bottom):")
    for element in s:
        print(element)