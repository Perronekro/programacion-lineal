class ArrayList:

    def __init__(self, size=100, initial_elements=None):
        if size <= 0:
            raise ValueError("Size must be greater than 0")

        self.capacity = size
        self.data = [None] * self.capacity
        self.count = 0

        if initial_elements:
            for element in initial_elements:
                self.append(element)

    def __str__(self):
        result = "["
        for i in range(self.count):
            result += str(self.data[i])
            if i < self.count - 1:
                result += ", "
        result += "]"
        return result

    def __len__(self):
        return self.count

    def isEmpty(self):
        return self.count == 0

    def __getitem__(self, index):
        if index < 0 or index >= self.count:
            raise IndexError("Index does not exist")
        return self.data[index]

    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        if self._iter_index < self.count:
            value = self.data[self._iter_index]
            self._iter_index += 1
            return value
        else:
            raise StopIteration

    def __contains__(self, element):
        for i in range(self.count):
            if self.data[i] == element:
                return True
        return False

    def append(self, element):
        if self.count >= self.capacity:
            raise OverflowError("ArrayList is full")

        self.data[self.count] = element
        self.count += 1

    def insert(self, index, element):
        if index < 0 or index > self.count:
            raise IndexError("Index does not exist")

        if self.count >= self.capacity:
            raise OverflowError("ArrayList is full")

        for i in range(self.count, index, -1):
            self.data[i] = self.data[i - 1]

        self.data[index] = element
        self.count += 1

    def remove(self, element):
        for i in range(self.count):
            if self.data[i] == element:
                self.pop(i)
                return
        raise ValueError("Element does not exist in the collection")

    def pop(self, index):
        if index < 0 or index >= self.count:
            raise IndexError("Index does not exist")

        removed = self.data[index]

        for i in range(index, self.count - 1):
            self.data[i] = self.data[i + 1]

        self.data[self.count - 1] = None
        self.count -= 1

        return removed

    def clear(self):
        for i in range(self.count):
            self.data[i] = None
        self.count = 0