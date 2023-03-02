import unittest
from FilterCollection import Query


class TestQuery_select(unittest.TestCase):
    def test_select(self):
        data = [1, 2, 3, 4]
        result = Query(data).select().get()
        self.assertEqual(data, result)


class TestQuery_where(unittest.TestCase):
    def test_where_numeric(self):
        data = [1, 2, 3, 4]
        result = Query(data).where(lambda x: x >= 3).get()
        self.assertEqual([3, 4], result)

    def test_where_attr(self):
        class Foo(object):
            def __init__(self, value):
                self.value = value

        data = [Foo("one"), Foo("two"), Foo("one")]
        result = Query(data).where("value", "one").get()
        self.assertEqual(len(result), 2)


class TestQuery_where_not(unittest.TestCase):
    def test_select(self):
        ...


class TestQuery__apply_where(unittest.TestCase):
    def test_select(self):
        ...


class TestQuery__apply_selects(unittest.TestCase):
    def test_select(self):
        ...


class TestQuery_get(unittest.TestCase):
    def test_select(self):
        ...


class TestQuery_exists(unittest.TestCase):
    def test_select(self):
        ...


class TestQuery_first(unittest.TestCase):
    def test_select(self):
        ...