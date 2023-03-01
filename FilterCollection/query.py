

class Query(object):
    op_funcs = {
        "==": lambda x, y: x == y,
        "!=": lambda x, y: x != y,
        ">=": lambda x, y: x >= y,
        "<=": lambda x, y: x <= y,
        ">": lambda x, y: x > y,
        "<": lambda x, y: x < y,
    }

    def __init__(self, data):
        self.data = data
        self._wheres = []
        self._selects = []

    def _handle_str_op(self, rval, op, lval):
        return self.op_funcs.get(op, lambda x, y: False)(rval, lval)

    def select(self, *args):
        self._selects.extend(args)
        return self

    def where(self, *args):
        self._wheres.append([*args, False])
        return self

    def where_not(self, *args):
        self._wheres.append([*args, True])
        return self

    def _apply_where(self, collection, where: tuple):
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

    def _apply_selects(self, collection):
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
        results = self.data

        for where in self._wheres:
            results = self._apply_where(results, where)

        return type(self.data)(self._apply_selects(results))

    def exists(self) -> bool:
        return not self.get().empty()

    def first(self):
        results = self.get()
        if len(results) > 0:
            return results[0]
        else:
            return None