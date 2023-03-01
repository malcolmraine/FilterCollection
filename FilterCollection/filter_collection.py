from __future__ import annotations
from copy import deepcopy
from query import Query


class FilterCollection(object):
    def __init__(self, data=None):
        if isinstance(data, FilterCollection):
            self.data = data.data
        else:
            self.data = data if data else []

    def __repr__(self):
        return f"FilterCollection({self.data})"

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __iter__(self):
        for item in self.data:
            yield item

    def __copy__(self):
        return self.__class__(deepcopy(self.data))

    def __add__(self, other):
        result = self.__copy__()
        result.extend(other)
        return result

    def __truediv__(self, other):
        result = FilterCollection()

        for item in other:
            if item in self:
                result.append(item)

        return result

    def unique(self):
        result = FilterCollection()

        for item in self:
            if item not in result:
                result.append(item)

        return result

    def sort(self, key=None):
        if key is None:
            self.data.sort()
        elif callable(key):
            self.data.sort(key=key)
        else:
            self.data.sort(key=lambda item: getattr(item, key))

    def to_list(self):
        return self.data

    def insert(self, index, item):
        self.data.insert(index, item)

    def append(self, item):
        self.data.append(item)

    def extend(self, items):
        if isinstance(items, list):
            self.data.extend(items)
        elif isinstance(items, FilterCollection):
            self.data.extend(items.to_list())

    def clear(self):
        self.data.clear()

    def empty(self):
        return len(self.data) == 0

    def query(self):
        return Query(self)

    def where(self, *args):
        return Query(self).where(*args)

    def where_not(self, *args):
        return Query(self).where_not(*args)

    def max(self, attr, get_item=False):
        if len(self.data) == 0:
            return None

        current_max_item = self.data[0]
        current_max_value = getattr(current_max_item, attr)
        for n in range(1, len(self.data)):
            value = getattr(self.data[n], attr)

            if value > current_max_value:
                current_max_value = value
                current_max_item = self.data[n]

        if get_item:
            return current_max_item
        else:
            return current_max_value


test = FilterCollection([1, 2, 3, 4])
print(test.query().where(lambda x: x >= 3).get())
