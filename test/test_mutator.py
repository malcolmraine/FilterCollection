import unittest
from Gatekeeper import Mutator


class Person(Mutator):
    def __init__(self):
        self.address = ""

    @staticmethod
    def get_address_attribute(value):
        # Using mutator without decorator
        return value.upper()


class TestMutator(unittest.TestCase):
    def test_cast(self) -> None:
        """
        Test for @Mutator.cast decorator.

        :return: None
        """

        @Mutator.cast(int)
        def func(x):
            return x

        self.assertEqual(55, func(55.989872))

    def test_upper(self) -> None:
        """
        Test for @Mutator.upper decorator.

        :return: None
        """

        @Mutator.upper
        def func(x):
            return x

        self.assertEqual("DOE", func("doe"))

    def test_lower(self) -> None:
        """
        Test @Mutator.lower decorator.

        :return: None
        """

        @Mutator.lower
        def func(x):
            return x

        self.assertEqual("john", func("JOHN"))

    def test_datetime(self) -> None:
        """
        Test for @Mutator.datetime decorator

        :return: None
        """

        @Mutator.datetime("%m/%d/%Y")
        def func(x):
            return x

        self.assertEqual("03/19/1983", func("1983-03-19T00:00:00Z"))

    def test_round(self) -> None:
        """
        Test for @Enforcer.round decorator.

        :return: None
        """

        @Mutator.round(2)
        def func(x):
            return x

        self.assertEqual(8.56, func(8.5587167847781))

    def test_saturate_low(self) -> None:
        """
        Test for @Enforcer.saturate decorator when the function argument
        falls below the given bounds.

        :return: None
        """

        @Mutator.saturate(0, 10)
        def func(x):
            return x

        self.assertEqual(0, func(-3))

    def test_saturate_high(self) -> None:
        """
        Test for @Enforcer.saturate decorator when the function argument
        falls above the given bounds.

        :return: None
        """

        @Mutator.saturate(0, 10)
        def func(x):
            return x

        self.assertEqual(10, func(15))

    def test_saturate_mid(self) -> None:
        """
        Test for @Enforcer.saturate decorator when the function argument
        falls between the given bounds.

        :return: None
        """

        @Mutator.saturate(0, 10)
        def func(x):
            return x

        self.assertEqual(8, func(8))

    def test_non_decorated(self) -> None:
        """
        Test for pass-through mutator method without a decorator.

        :return: None
        """
        person = Person()
        person.address = "123 abc lane"

        self.assertEqual("123 ABC LANE", person.address)
