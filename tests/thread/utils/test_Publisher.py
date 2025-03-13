import unittest

from safethread.thread.utils import Publisher, Subscriber


class TestPublisher(unittest.TestCase):
    """Unit tests for the Publisher class."""

    def setUp(self) -> None:
        super().setUp()
        self.result = "Hello from "

        def replace_result_with(data):
            self.result = data

        def append_to_result(data):
            self.result = self.result + data

        self.subscriber1 = Subscriber(replace_result_with)
        self.subscriber2 = Subscriber(append_to_result)

        self.publisher = Publisher()
        self.publisher.subscribe(self.subscriber1)
        self.publisher.subscribe(self.subscriber2)

    def test_publish(self):
        """Test if publisher and subscriber work correctly together."""
        test_data = "New Data "
        self.publisher.publish(test_data)
        self.assertEqual(self.result, "New Data New Data ")

    def test_unsubscribe(self):
        """Test if publisher and subscriber work correctly together."""
        self.publisher.unsubscribe(self.subscriber1)

        test_data = "TestUnit"
        self.publisher.publish(test_data)
        self.assertEqual(self.result, "Hello from TestUnit")
