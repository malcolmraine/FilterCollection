"""
MIT License

Copyright (c) 2023 Malcolm Hall

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
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
        """

        Returns
        -------

        """
        return f"FilterCollection({self.data})"

    def __len__(self):
        """

        Returns
        -------

        """
        return len(self.data)

    def __getitem__(self, item):
        """

        Parameters
        ----------
        item

        Returns
        -------

        """
        return self.data[item]

    def __setitem__(self, key, value):
        """

        Parameters
        ----------
        key
        value

        Returns
        -------

        """
        self.data[key] = value

    def __iter__(self):
        """

        Returns
        -------

        """
        for item in self.data:
            yield item

    def __copy__(self):
        """

        Returns
        -------

        """
        return self.__class__(deepcopy(self.data))

    def __add__(self, other):
        """

        Parameters
        ----------
        other

        Returns
        -------

        """
        result = self.__copy__()
        result.extend(other)
        return result

    def __truediv__(self, other):
        """

        Parameters
        ----------
        other

        Returns
        -------

        """
        result = FilterCollection()

        for item in other:
            if item in self:
                result.append(item)

        return result

    def unique(self):
        """

        Returns
        -------

        """
        result = FilterCollection()

        for item in self:
            if item not in result:
                result.append(item)

        return result

    def sort(self, key=None):
        """

        Parameters
        ----------
        key

        Returns
        -------

        """
        if key is None:
            self.data.sort()
        elif callable(key):
            self.data.sort(key=key)
        else:
            self.data.sort(key=lambda item: getattr(item, key))

    def to_list(self):
        """

        Returns
        -------

        """
        return self.data

    def insert(self, index, item):
        """

        Parameters
        ----------
        index
        item

        Returns
        -------

        """
        self.data.insert(index, item)

    def append(self, item):
        """

        Parameters
        ----------
        item

        Returns
        -------

        """
        self.data.append(item)

    def extend(self, items):
        """

        Parameters
        ----------
        items

        Returns
        -------

        """
        if isinstance(items, list):
            self.data.extend(items)
        elif isinstance(items, FilterCollection):
            self.data.extend(items.to_list())

    def clear(self):
        """

        Returns
        -------

        """
        self.data.clear()

    def empty(self):
        """

        Returns
        -------

        """
        return len(self.data) == 0

    def query(self):
        """

        Returns
        -------

        """
        return Query(self)

    def where(self, *args):
        """

        Parameters
        ----------
        args

        Returns
        -------

        """
        return Query(self).where(*args)

    def where_not(self, *args):
        """

        Parameters
        ----------
        args

        Returns
        -------

        """
        return Query(self).where_not(*args)

    def max(self, attr, get_item=False):
        """

        Parameters
        ----------
        attr
        get_item

        Returns
        -------

        """
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
