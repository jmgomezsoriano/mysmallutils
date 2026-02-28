import unittest

from mysutils.misc import conditional, retry
import unittest
from unittest.mock import MagicMock


class TestRetryDecorator(unittest.TestCase):

    def test_success_immediate(self):
        """Should return the result immediately if no exception occurs."""
        mock_func = MagicMock(return_value="OK")
        decorated = retry(retries=3, delay=0)(mock_func)

        result = decorated()

        self.assertEqual(result, "OK")
        self.assertEqual(mock_func.call_count, 1)

    def test_success_after_retries(self):
        """Should succeed if the function eventually returns a value within retry limit."""
        # Simulamos que falla 2 veces y funciona a la 3ra
        mock_func = MagicMock(side_effect=[ValueError("Err1"), ValueError("Err2"), "Success"])
        decorated = retry(retries=3, delay=0, exceptions=ValueError)(mock_func)

        result = decorated()

        self.assertEqual(result, "Success")
        self.assertEqual(mock_func.call_count, 3)

    def test_exhaust_retries_raises_exception(self):
        """Should raise the last exception after all attempts are exhausted."""
        mock_func = MagicMock(side_effect=ZeroDivisionError("Division by zero"))
        decorated = retry(retries=3, delay=0, exceptions=ZeroDivisionError)(mock_func)

        with self.assertRaises(ZeroDivisionError):
            decorated()

        self.assertEqual(mock_func.call_count, 3)

    def test_unhandled_exception_raises_immediately(self):
        """Should not retry if an exception occurs that is not in the 'exceptions' list."""
        # Configuramos para que solo reintente ValueError, pero lanzamos TypeError
        mock_func = MagicMock(side_effect=TypeError("Not handled"))
        decorated = retry(retries=5, delay=0, exceptions=ValueError)(mock_func)

        with self.assertRaises(TypeError):
            decorated()

        # Debe fallar al primer intento sin reintentar
        self.assertEqual(mock_func.call_count, 1)


def my_func(a: int, b: str, **kwargs) -> str:
    return f'Intent {a} of {b} for {kwargs["c"]}'


class MyTestCase(unittest.TestCase):
    def test_conditional(self):
        self.assertEqual(conditional(my_func, 3 > 2, 1, 'apple', c='Lucas'), 'Intent 1 of apple for Lucas')
        self.assertIsNone(conditional(my_func, 3 < 2, 1, 'apple', c='Lucas'), 'Intent 1 of apple for Lucas')



if __name__ == '__main__':
    unittest.main()
