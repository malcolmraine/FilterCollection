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
from typing import Any, Union, Iterable


class Query(object):
    op_funcs: dict = {
        "==": lambda x, y: x == y,
        "!=": lambda x, y: x != y,
        ">=": lambda x, y: x >= y,
        "<=": lambda x, y: x <= y,
        ">": lambda x, y: x > y,
        "<": lambda x, y: x < y,
    }

    def __init__(self, data):
        self.data = data
        self._wheres: list = []
        self._selects: list = []

    def _handle_str_op(self, rval: Any, op: str, lval: Any):
        """
        Perform a binary operation on two values.

        Parameters
        ----------
        rval
        op
        lval

        Returns
        -------
        Binary operation result.
        """
        return self.op_funcs.get(op, lambda x, y: False)(rval, lval)

    def select(self, *args) -> Query:
        """
        Add an attribute selection to the query.

        Parameters
        ----------
        args
            Attributes to select.

        Returns
        -------
        Query
        """
        self._selects.extend(args)
        return self

    def where(self, *args) -> Query:
        """
        Add a where operations to a collection.

        Parameters
        ----------
        args
            L-value, operator, R-value or L-value and R-value for equality.

        Returns
        -------
        Query
        """
        self._wheres.append([*args, False])
        return self

    def where_not(self, *args) -> Query:
        """
        Add a where-not operations to a collection.

        Parameters
        ----------
        args
            L-value, operator, R-value or L-value and R-value for equality.

        Returns
        -------
        Query
        """
        self._wheres.append([*args, True])
        return self

    def _apply_where(self, collection, where: tuple) -> list:
        """
        Apply where operations to a collection.

        Parameters
        ----------
        collection
            Collection to apply where operations to.
        where: tuple
            R-value, operator, and L-value of where operation.

        Returns
        -------
        list
        """
        results = []
        invert = where[-1]

        for item in collection:
            include_item = False
            if callable(where[0]):
                rval = where[0](item)
            else:
                rval = getattr(item, where[0])

            if len(where) == 2:
                include_item = bool(rval)
            elif len(where) == 3:
                include_item = rval == where[1]
            elif len(where) == 4:
                include_item = self._handle_str_op(rval, where[1], where[2])

            if invert and not include_item:
                results.append(item)
            elif include_item and not invert:
                results.append(item)

        return results

    def _apply_selects(self, collection) -> list:
        """
        Apply the attribute selections to a collection.

        Parameters
        ----------
        collection
            Collection to apply selections to.

        Returns
        -------
        list
        """
        if len(self._selects) == 0:
            return collection

        results = []
        for item in collection:
            result = dict()
            for attr in self._selects:
                result[attr] = getattr(item, attr)

            results.append(result)

        return results

    def get(self):
        """
        Get the results of a query.

        Returns
        -------
        Union[Iterable, FilterCollection]
        """
        results = self.data
        for where in self._wheres:
            results = self._apply_where(results, where)

        return type(self.data)(self._apply_selects(results))

    def exists(self) -> bool:
        """
        Checks whether the result of a query produces any results.

        Returns
        -------
        bool
        """
        return len(self.get()) > 0

    def first(self) -> Any:
        """
        Gets the first item from the query results.

        Returns
        -------
        Any
        """
        results = self.get()
        if len(results) > 0:
            return results[0]
        else:
            return None
