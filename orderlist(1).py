class CustomList:
    
    def __init__(self, data=None):
        self._data = list(data) if data is not None else []
    
    def __repr__(self):
        return f"CustomList({self._data})"
    
    def __len__(self):
        return len(self._data)
    
    def __getitem__(self, index):
        try:
            return self._data[index]
        except IndexError:
            raise IndexError("Index out of range.")
    
    def __contains__(self, value):
        return value in self._data
    
    def __iter__(self):
        for item in self._data:
            yield item
    
    def empty(self):
        return len(self._data) == 0
    
    def append(self, value):
        self._data.append(value)
    
    def delete(self, value):
        try:
            self._data.remove(value)
        except ValueError:
            raise ValueError("Value not found in list.")
    
    def pop(self, index=-1):
        try:
            return self._data.pop(index)
        except IndexError:
            raise IndexError("Index out of range.")
    
    def reset(self):
        self._data.clear()


# prueba diferente
if __name__ == "__main__":
    my_list = CustomList([5, 15, 25])
    print("Original:", my_list)

    my_list.append(35)
    print("After append:", my_list)

    print("First element:", my_list[0])
    print("Contains 15?", 15 in my_list)

    print("Iterating:")
    for val in my_list:
        print(val)

    my_list.delete(15)
    print("After delete:", my_list)

    print("Pop last:", my_list.pop())
    print("After pop:", my_list)

    my_list.reset()
    print("After reset:", my_list)
    print("Is empty?", my_list.empty())