import unittest

from safethread.thread.utils import ThreadSubscriber


class TestThreadSubscriber(unittest.TestCase):
    """Unit tests for the Subscriber class."""

    def test_subscriber_with_invalid_callback(self):
        """Test if the subscriber raises an error when initialized with a non-callable callback."""
        with self.assertRaises(TypeError):
            ThreadSubscriber("not_a_function")   # type: ignore

    def test_subscriber_receives_notification(self):
        """Test if the subscriber receives notifications correctly."""
        self.result = 0

        def callback(data):
            print(data)
            self.result = data+5

        subscriber = ThreadSubscriber(callback)

        test_data = 10
        subscriber._notify(test_data)
        self.assertEqual(self.result, 15)

        test_data = 50.2
        subscriber._notify(test_data)
        self.assertEqual(self.result, 55.2)


if __name__ == "__main__":
    unittest.main()
