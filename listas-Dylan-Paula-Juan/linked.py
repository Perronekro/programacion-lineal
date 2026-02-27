class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:

    def __init__(self, initial_elements=None):
        self.head = None
        self.count = 0

        if initial_elements:
            for element in initial_elements:
                self.append(element)

    def __str__(self):
        result = "["
        current = self.head
        while current:
            result += str(current.data)
            if current.next:
                result += ", "
            current = current.next
        result += "]"
        return result

    def __len__(self):
        return self.count

    def isEmpty(self):
        return self.head is None

    def __getitem__(self, index):
        if index < 0 or index >= self.count:
            raise IndexError("Index does not exist")

        current = self.head
        for _ in range(index):
            current = current.next

        return current.data

    def append(self, element):
        new_node = Node(element)

        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

        self.count += 1

    def insert(self, index, element):
        if index < 0 or index > self.count:
            raise IndexError("Index does not exist")

        new_node = Node(element)

        if index == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            for _ in range(index - 1):
                current = current.next

            new_node.next = current.next
            current.next = new_node

        self.count += 1

    def remove(self, element):
        if self.head is None:
            raise ValueError("Element does not exist")

        if self.head.data == element:
            self.head = self.head.next
            self.count -= 1
            return

        current = self.head
        while current.next and current.next.data != element:
            current = current.next

        if current.next is None:
            raise ValueError("Element does not exist")

        current.next = current.next.next
        self.count -= 1

    def pop(self, index):
        if index < 0 or index >= self.count:
            raise IndexError("Index does not exist")

        if index == 0:
            removed = self.head.data
            self.head = self.head.next
            self.count -= 1
            return removed

        current = self.head
        for _ in range(index - 1):
            current = current.next

        removed = current.next.data
        current.next = current.next.next
        self.count -= 1
        return removed

    def clear(self):
        self.head = None
        self.count = 0