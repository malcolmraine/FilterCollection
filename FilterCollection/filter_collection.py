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
from .query import Query
from typing import Iterable, Any, Union


class FilterCollection(object):
    def __init__(self, data=None):
        if isinstance(data, FilterCollection):
            self.data = data.data
        else:
            self.data = data if data else []

    def __repr__(self):
        """
        Implementation of __repr__ magic method.

        Returns
        -------
        str
        """
        return f"FilterCollection({self.data})"

    def __len__(self) -> int:
        """
        Implementation of __len__ magic method.

        Returns
        -------
        int
        """
        return len(self.data)

    def __getitem__(self, item: int):
        """
        Implementation of __getitem__ magic method.

        Parameters
        ----------
        item: int
            Index of the value to get.

        Returns
        -------
        Any
        """
        return self.data[item]

    def __setitem__(self, key: int, value: Any) -> None:
        """
        Implementation of __getitem__ magic method.

        Parameters
        ----------
        key: int
        value: Any

        Returns
        -------
        None
        """
        self.data[key] = value

    def __iter__(self) -> Any:
        """
        Implementation of __iter__ magic method.

        Returns
        -------
        An item from the list.
        """
        for item in self.data:
            yield item

    def __copy__(self) -> FilterCollection:
        """
        Implementation of __copy__ magic method.

        Returns
        -------
        FilterCollection
        """
        return self.__class__(deepcopy(self.data))

    def __add__(self, other: Union[Iterable, FilterCollection]) -> FilterCollection:
        """
        Implementation of __add__ magic method. Extends the collection
        using the data from the provided argument.

        Parameters
        ----------
        other: list or set or FilterCollection

        Returns
        -------
        FilterCollection
        """
        result = self.__copy__()
        result.extend(other)
        return result

    def __truediv__(self, other: Union[Iterable, FilterCollection]) -> FilterCollection:
        """
        Implementation of __truediv__ magic method. Returns the set intersection.

        Parameters
        ----------
        other: Union[Iterable, FilterCollection]
            Other collection or iterable to intersect with.

        Returns
        -------
        FilterCollection
        """
        result = FilterCollection()

        for item in other:
            if item in self:
                result.append(item)

        return result

    def unique(self) -> FilterCollection:
        """
        Return only unique values in collection.

        Returns
        -------
        FilterCollection
        """
        result = FilterCollection()
        for item in self:
            if item not in result:
                result.append(item)

        return result

    def sort(self, key=None) -> FilterCollection:
        """
        Sort the collection.

        Parameters
        ----------
        key
            Sort-by key.

        Returns
        -------
        FilterCollection
        """
        if key is None:
            self.data.sort()
        elif callable(key):
            self.data.sort(key=key)
        else:
            self.data.sort(key=lambda item: getattr(item, key))
        return self

    def to_list(self) -> list:
        """
        Convert collection to native list form.

        Returns
        -------
        list
        """
        return self.data

    def insert(self, index: int, item: Any) -> FilterCollection:
        """
        Insert an item at the specified index.

        Parameters
        ----------
        index: int
            Index to insert item at.
        item: Any
            Item to insert

        Returns
        -------
        FilterCollection
        """
        self.data.insert(index, item)
        return self

    def append(self, item: Any) -> FilterCollection:
        """

        Parameters
        ----------
        item

        Returns
        -------

        """
        self.data.append(item)
        return self

    def extend(self, items: Union[Iterable, FilterCollection]) -> FilterCollection:
        """
        Extend the collection using the provided data.

        Parameters
        ----------
        items: Union[Iterable, FilterCollection]
            Items to add to collection.

        Returns
        -------
        FilterCollection
        """
        if isinstance(items, list):
            self.data.extend(items)
        elif isinstance(items, FilterCollection):
            self.data.extend(items.to_list())
        return self

    def clear(self) -> None:
        """
        Clear the collection data.

        Returns
        -------
        None
        """
        self.data.clear()

    def empty(self) -> bool:
        """
        Check whether the collection is empty.

        Returns
        -------
        bool
        """
        return len(self.data) == 0

    def query(self) -> Query:
        """
        Query the collection.

        Returns
        -------
        Query
        """
        return Query(self)

    def where(self, *args) -> Query:
        """
        Create a query against the collection with a where clause.

        Parameters
        ----------
        args
            Arguments to provide the query.

        Returns
        -------
        Query
        """
        return Query(self).where(*args)

    def where_not(self, *args) -> Query:
        """
        Create a query against the collection with a where-not clause.

        Parameters
        ----------
        args
            Arguments to provide the query.

        Returns
        -------
        Query
        """
        return Query(self).where_not(*args)

    def max(self, attr: str, get_item: bool = False) -> Any:
        """
        Get the result with the maximum value for the given attribute.

        Parameters
        ----------
        attr: str
            Attribute to use for comparison.
        get_item: bool
            Flag indicating whether the item itself should be returned or the
            maximum value.

        Returns
        -------
        Any
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
