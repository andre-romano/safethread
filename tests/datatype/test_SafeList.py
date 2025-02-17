import unittest
import threading

from safethread.datatype import SafeList


class TestSafeList(unittest.TestCase):

    def setUp(self):
        """Set up a new SafeList instance for each test."""
        self.safe_list = SafeList()

    def test_initialization(self):
        safe_list = SafeList([])
        self.assertEqual(safe_list._data, [])

        safe_list = SafeList([1, 2])
        self.assertEqual(safe_list, [1, 2])

        safe_list = SafeList((5, 7))
        self.assertEqual(safe_list[0], 5)
        self.assertEqual(safe_list[1], 7)

    def test_empty(self):
        self.assertEqual(self.safe_list._data, [])
        self.assertEqual(self.safe_list, SafeList([]))

    def test_non_empty(self):
        """Test creating non-empty list."""
        self.safe_list = SafeList([1])
        self.assertEqual(self.safe_list._data, [1])
        self.assertEqual(self.safe_list, SafeList([1]))

    def test_append(self):
        """Test appending elements to the list."""
        self.safe_list.append(1)
        self.safe_list.append(2)
        self.assertEqual(self.safe_list._data, [1, 2])

        self.assertEqual(self.safe_list[0], 1)
        self.assertEqual(self.safe_list[1], 2)

    def test_clear(self):
        """Test clearing the list."""
        self.safe_list.append(1)
        self.safe_list.append(2)
        self.safe_list.clear()
        self.assertEqual(self.safe_list._data, [])

    def test_count(self):
        """Test counting occurrences of an element."""
        self.safe_list.extend([1, 2, 2, 3, 2])
        self.assertEqual(self.safe_list.count(2), 3)

    def test_extend(self):
        """Test extending the list."""
        self.safe_list.append(1)
        self.safe_list.extend([2, 3])
        self.assertEqual(self.safe_list._data, [1, 2, 3])

    def test_index(self):
        """Test finding index of an element."""
        self.safe_list.extend([10, 20, 30, 40])
        self.assertEqual(self.safe_list.index(30), 2)

    def test_insert(self):
        """Test inserting an element."""
        self.safe_list.extend([1, 3])
        self.safe_list.insert(1, 2)
        self.assertEqual(self.safe_list._data, [1, 2, 3])

    def test_pop(self):
        """Test popping an element."""
        self.safe_list.extend([1, 2, 3])
        self.assertEqual(self.safe_list.pop(), 3)
        self.assertEqual(self.safe_list._data, [1, 2])

        self.assertEqual(self.safe_list.pop(0), 1)
        self.assertEqual(self.safe_list._data, [2])

    def test_remove(self):
        """Test removing an element."""
        self.safe_list.extend([1, 2, 3])
        self.safe_list.remove(2)
        self.assertEqual(self.safe_list._data, [1, 3])

    def test_reverse(self):
        """Test reversing the list."""
        self.safe_list.extend([1, 2, 3])
        self.safe_list.reverse()
        self.assertEqual(self.safe_list._data, [3, 2, 1])

    def test_sort(self):
        """Test sorting the list."""
        self.safe_list.extend([3, 1, 2])
        self.safe_list.sort()
        self.assertEqual(self.safe_list._data, [1, 2, 3])

    def test_thread_safety(self):
        """Test SafeList with multiple threads appending elements."""
        def worker(lst: SafeList, values: int):
            for value in range(values):
                lst.append(value)

        threads = []
        n_threads, values = 10, 100
        for _ in range(n_threads):  # n_threads threads appending numbers 0-values
            thread = threading.Thread(
                target=worker, args=(self.safe_list, values))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # len(threads) * values = 1000 elements
        self.assertEqual(len(self.safe_list._data), n_threads*values)


if __name__ == '__main__':
    unittest.main()
