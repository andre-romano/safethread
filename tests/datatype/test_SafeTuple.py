import unittest
import threading

from safethread.datatype import SafeTuple


class TestSafeTuple(unittest.TestCase):

    def setUp(self):
        """Set up a thread-safe tuple for testing."""
        self.safe_tuple = SafeTuple((1, 2, 3, 2, 4, 2))

    def test_initialization(self):
        safe_tuple = SafeTuple([5, 5, 6, 7])
        self.assertEqual(safe_tuple.count(2), 0)
        self.assertEqual(safe_tuple.count(5), 2)

        safe_tuple = SafeTuple()
        self.assertEqual(safe_tuple.count(1), 0)
        self.assertEqual(len(safe_tuple), 0)

    def test_count(self):
        """Test the count method for correct results."""
        # Count occurrences of 2 in the tuple (should be 3)
        self.assertEqual(self.safe_tuple.count(2), 3)

        # Count occurrences of 5 in the tuple (should be 0)
        self.assertEqual(self.safe_tuple.count(5), 0)

    def test_index(self):
        """Test the index method for correct results."""
        # Get the index of the first occurrence of 2 in the tuple (should be 1)
        self.assertEqual(self.safe_tuple.index(2), 1)

        # Get the index of the first occurrence of 3 in the tuple (should be 2)
        self.assertEqual(self.safe_tuple.index(3), 2)

        # Get the index with a start and end range
        self.assertEqual(self.safe_tuple.index(2, 2), 3)

        # Test for value that doesn't exist, should raise ValueError
        with self.assertRaises(ValueError):
            self.safe_tuple.index(5)

    def test_thread_safety(self):
        """Test the thread safety of the methods."""
        def count_test():
            self.assertEqual(self.safe_tuple.count(2), 3)

        def index_test():
            self.assertEqual(self.safe_tuple.index(2), 1)

        # Create multiple threads to test thread safety
        threads = []
        for _ in range(10):
            t1 = threading.Thread(target=count_test)
            t2 = threading.Thread(target=index_test)
            threads.extend([t1, t2])
            t1.start()
            t2.start()

        for t in threads:
            t.join()


if __name__ == '__main__':
    unittest.main()
