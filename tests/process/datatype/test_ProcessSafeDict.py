import unittest
import multiprocessing

from multiprocessing.managers import DictProxy
from typing import Any

from safethread.process.datatype import ProcessSafeDict


def worker(d: ProcessSafeDict, key: str, value: int):
    d[key] = value


def worker_two(d: ProcessSafeDict, key: str, value: int):
    with d.get_lock():
        d[key] = value


class TestProcessSafeDict(unittest.TestCase):
    def test_initialization(self):
        """
        Test that the dictionary is initialized correctly.
        """
        # Test initialization with no data
        safe_dict = ProcessSafeDict()
        self.assertIsInstance(safe_dict._data, DictProxy)
        self.assertEqual(len(safe_dict), 0)

        # Test initialization with a dictionary
        safe_dict = ProcessSafeDict({"a": 1, "b": 2})
        self.assertIsInstance(safe_dict._data, DictProxy)
        self.assertEqual(len(safe_dict), 2)
        self.assertEqual(safe_dict["a"], 1)
        self.assertEqual(safe_dict["b"], 2)

        # Test initialization with an iterable
        safe_dict = ProcessSafeDict([("a", 1), ("b", 2)])
        self.assertIsInstance(safe_dict._data, DictProxy)
        self.assertEqual(len(safe_dict), 2)
        self.assertEqual(safe_dict["a"], 1)
        self.assertEqual(safe_dict["b"], 2)

        # Test initialization with another ProcessSafeDict
        safe_dict = ProcessSafeDict(safe_dict)
        self.assertIsInstance(safe_dict._data, DictProxy)
        self.assertEqual(len(safe_dict), 2)
        self.assertEqual(safe_dict["a"], 1)
        self.assertEqual(safe_dict["b"], 2)

    def test_basic_operations(self):
        """
        Test basic dictionary operations.
        """
        safe_dict = ProcessSafeDict()

        # Test __setitem__ and __getitem__
        safe_dict["a"] = 1
        self.assertEqual(safe_dict["a"], 1)

        # Test __delitem__
        safe_dict["b"] = 2
        del safe_dict["b"]
        with self.assertRaises(KeyError):
            _ = safe_dict["b"]

        # Test __len__
        self.assertEqual(len(safe_dict), 1)

    def test_concurrent_access(self):
        """
        Test that concurrent access by multiple processes is safe.
        """
        safe_dict = ProcessSafeDict()

        # Create multiple processes
        processes = [
            multiprocessing.Process(
                target=worker, args=(safe_dict, f"key_{i}", i))
            for i in range(10)
        ]

        # Start all processes
        for process in processes:
            process.start()

        # Wait for all processes to finish
        for process in processes:
            process.join()

        # Verify that all keys were added correctly
        self.assertEqual(len(safe_dict), 10)
        for i in range(10):
            self.assertEqual(safe_dict[f"key_{i}"], i)

    def test_concurrent_access_two(self):
        """
        Test that concurrent access by multiple processes is safe.
        """
        safe_dict = ProcessSafeDict()

        # Create multiple processes
        processes = [
            multiprocessing.Process(
                target=worker_two, args=(safe_dict, f"key_{i}", i))
            for i in range(10)
        ]

        # Start all processes
        for process in processes:
            process.start()

        # Wait for all processes to finish
        for process in processes:
            process.join()

        # Verify that all keys were added correctly
        self.assertEqual(len(safe_dict), 10)
        for i in range(10):
            self.assertEqual(safe_dict[f"key_{i}"], i)

    def test_edge_cases(self):
        """
        Test edge cases such as empty dictionaries and non-existent keys.
        """
        safe_dict = ProcessSafeDict()

        # Test access to non-existent key
        with self.assertRaises(KeyError):
            _ = safe_dict["non_existent_key"]

        # Test deletion of non-existent key
        with self.assertRaises(KeyError):
            del safe_dict["non_existent_key"]

        # Test empty dictionary
        self.assertEqual(len(safe_dict), 0)


if __name__ == "__main__":
    unittest.main()
