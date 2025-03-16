import unittest
import unittest.mock

from safethread.utils.utils import is_callable, try_except_finally_wrap


class TestUtils(unittest.TestCase):

    def test_is_callable_with_function(self):
        def sample_function():
            pass
        self.assertEqual(is_callable(sample_function), sample_function)

    def test_is_callable_with_lambda(self):
        def sample_lambda(): return None
        self.assertEqual(is_callable(sample_lambda), sample_lambda)

    def test_is_callable_with_non_callable(self):
        with self.assertRaises(TypeError):
            is_callable(123)  # type: ignore

    def test_try_except_finally_wrap_success(self):
        callback = unittest.mock.Mock()
        callback_succ = unittest.mock.Mock()
        callback_fail = unittest.mock.Mock()
        callback_final = unittest.mock.Mock()

        try_except_finally_wrap(
            callback,
            callback_succ=callback_succ,
            callback_fail=callback_fail,
            callback_final=callback_final,
        )

        callback.assert_called_once()
        callback_succ.assert_called_once()
        callback_fail.assert_not_called()
        callback_final.assert_called_once()

    def test_try_except_finally_wrap_failure(self):
        def callback():
            raise Exception("Test exception")
        callback_succ = unittest.mock.Mock()
        callback_fail = unittest.mock.Mock()
        callback_final = unittest.mock.Mock()

        try_except_finally_wrap(
            callback,
            callback_succ=callback_succ,
            callback_fail=callback_fail,
            callback_final=callback_final,
        )

        callback_succ.assert_not_called()
        callback_fail.assert_called_once()
        callback_final.assert_called_once()

    def test_try_except_finally_wrap_finally(self):
        callback = unittest.mock.Mock()
        callback_final = unittest.mock.Mock()

        try_except_finally_wrap(
            callback,
            callback_final=callback_final,
        )

        callback.assert_called_once()
        callback_final.assert_called_once()


if __name__ == '__main__':
    unittest.main()
