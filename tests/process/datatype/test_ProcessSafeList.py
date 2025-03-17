
import unittest
import multiprocessing

from multiprocessing.managers import ListProxy
from typing import Any

from safethread.process.datatype import ProcessSafeList


def worker(lst: ProcessSafeList, value: int):
    lst.append(value)


def worker_two(lst: ProcessSafeList, value: int):
    with lst.get_lock():  # Ensure thread safety for the test
        lst.append(value)


class TestProcessSafeList(unittest.TestCase):
    def test_initialization(self):
        """
        Test that the list is initialized correctly.
        """
        # Test initialization with no data
        safe_list = ProcessSafeList()
        self.assertIsInstance(safe_list._data, ListProxy)
        self.assertEqual(len(safe_list._data), 0)
        self.assertEqual(len(safe_list), 0)

        # Test initialization with a list
        safe_list = ProcessSafeList([1, 2, 3])
        self.assertIsInstance(safe_list._data, ListProxy)
        self.assertEqual(len(safe_list._data), 3)
        self.assertEqual(len(safe_list), 3)
        self.assertEqual(safe_list[0], 1)
        self.assertEqual(safe_list[1], 2)
        self.assertEqual(safe_list[2], 3)

        # Test initialization with an iterable
        safe_list = ProcessSafeList((1, 2, 3))
        self.assertIsInstance(safe_list._data, ListProxy)
        self.assertEqual(len(safe_list), 3)
        self.assertEqual(safe_list[0], 1)
        self.assertEqual(safe_list[1], 2)
        self.assertEqual(safe_list[2], 3)

        # Test initialization with a ListProxy
        list_p = multiprocessing.Manager().list((1, 2, 3))
        safe_list = ProcessSafeList(list_p)
        self.assertIsInstance(safe_list._data, ListProxy)
        self.assertEqual(len(safe_list), 3)
        self.assertEqual(safe_list[0], 1)
        self.assertEqual(safe_list[1], 2)
        self.assertEqual(safe_list[2], 3)

        # Test initialization with another ProcessSafeList
        safe_list = ProcessSafeList(safe_list)
        self.assertIsInstance(safe_list._data, ListProxy)
        self.assertEqual(len(safe_list), 3)
        self.assertEqual(safe_list[0], 1)
        self.assertEqual(safe_list[1], 2)
        self.assertEqual(safe_list[2], 3)

    def test_basic_operations(self):
        """
        Test basic list operations.
        """
        safe_list = ProcessSafeList()

        # Test append
        safe_list.append(1)
        self.assertEqual(safe_list[0], 1)
        self.assertEqual(safe_list[0], 1)

        # Test clear
        safe_list.clear()
        self.assertEqual(len(safe_list), 0)
        self.assertEqual(len(safe_list), 0)

        # Test count
        safe_list.extend([1, 2, 2, 3])
        self.assertEqual(safe_list.count(2), 2)

        # Test extend
        safe_list.extend([4, 5])
        self.assertEqual(len(safe_list), 6)
        self.assertEqual(safe_list[4], 4)

        # Test index
        self.assertEqual(safe_list.index(3), 3)

        # Test insert
        safe_list.insert(0, 0)
        self.assertEqual(len(safe_list), 7)
        self.assertEqual(safe_list[0], 0)

        # Test pop
        self.assertEqual(safe_list.pop(), 5)
        self.assertEqual(len(safe_list), 6)

        # Test remove
        safe_list.remove(2)
        self.assertEqual(safe_list.count(2), 1)

        # Test reverse
        safe_list.reverse()
        self.assertEqual(safe_list[0], 4)

        # Test sort
        safe_list.sort()
        self.assertEqual(safe_list[0], 0)

    def test_concurrent_access(self):
        """
        Test that concurrent access by multiple processes is safe.
        """
        safe_list = ProcessSafeList()

        # Create multiple processes
        processes = [
            multiprocessing.Process(target=worker, args=(safe_list, i))
            for i in range(10)
        ]

        # Start all processes
        for process in processes:
            process.start()

        # Wait for all processes to finish
        for process in processes:
            process.join()

        # Verify that all values were added correctly
        self.assertEqual(len(safe_list), 10)
        for i in range(10):
            self.assertIn(i, safe_list)

    def test_concurrent_access_two(self):
        """
        Test that concurrent access by multiple processes is safe.
        """
        safe_list = ProcessSafeList()

        # Create multiple processes
        processes = [
            multiprocessing.Process(target=worker_two, args=(safe_list, i))
            for i in range(10)
        ]

        # Start all processes
        for process in processes:
            process.start()

        # Wait for all processes to finish
        for process in processes:
            process.join()

        # Verify that all values were added correctly
        self.assertEqual(len(safe_list), 10)
        for i in range(10):
            self.assertIn(i, safe_list)

    def test_edge_cases(self):
        """
        Test edge cases such as empty lists and non-existent items.
        """
        safe_list = ProcessSafeList()

        # Test pop from empty list
        with self.assertRaises(IndexError):
            safe_list.pop()

        # Test remove non-existent item
        with self.assertRaises(ValueError):
            safe_list.remove(42)

        # Test index of non-existent item
        with self.assertRaises(ValueError):
            safe_list.index(42)


if __name__ == "__main__":
    unittest.main()
