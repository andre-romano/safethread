import unittest
import threading

from safethread.thread.datatype import ThreadSafeDict


class TestSafeThreadDict(unittest.TestCase):

    def setUp(self):
        """Initialize a SafeDictThread instance before each test."""
        self.safe_dict = ThreadSafeDict({'a': 1, 'b': 2, 'c': 3})

    def test_initialize(self):
        safe_dict = ThreadSafeDict()
        self.assertTrue(len(safe_dict) == 0)

        safe_dict = ThreadSafeDict([('a', 1), ('b', 2)])
        self.assertTrue(safe_dict['a'] == 1)
        self.assertTrue(safe_dict['b'] == 2)

    def test_clear(self):
        """Test if clear() empties the dictionary."""
        self.safe_dict.clear()
        self.assertTrue(len(self.safe_dict._data) == 0)
        self.assertTrue(len(self.safe_dict) == 0)

    def test_fromkeys(self):
        """Test if fromkeys() correctly creates a dictionary."""
        result = self.safe_dict.fromkeys(['x', 'y', 'z'], 0)
        self.assertTrue(result == {'x': 0, 'y': 0, 'z': 0})
        self.assertTrue('x' not in self.safe_dict)
        self.assertTrue('x' not in self.safe_dict._data)

    def test_get(self):
        """Test if get() retrieves values safely."""
        self.assertTrue(self.safe_dict.get('a') == 1)
        self.assertTrue(self.safe_dict.get('z', 99) == 99)

        self.assertTrue(self.safe_dict['a'] == 1)
        with self.assertRaises(Exception):
            _ = self.safe_dict['z']

    def test_items(self):
        """Test if items() returns key-value pairs."""
        self.assertTrue(
            set(self.safe_dict.items()) ==
            {('a', 1), ('b', 2), ('c', 3)}
        )

    def test_keys(self):
        """Test if keys() returns dictionary keys."""
        self.assertTrue(
            set(self.safe_dict.keys()) ==
            {'a', 'b', 'c'}
        )

    def test_pop(self):
        """Test if pop() removes a key and returns its value."""
        self.assertTrue(self.safe_dict.pop('b') == 2)
        self.assertTrue('b' not in self.safe_dict._data)
        self.assertTrue('b' not in self.safe_dict)

        self.assertTrue(self.safe_dict.pop('z', 100) == 100)

    def test_popitem(self):
        """Test if popitem() removes and returns the last key-value pair."""
        key, value = self.safe_dict.popitem()
        self.assertTrue(key not in self.safe_dict)

    def test_popitem_empty(self):
        """Test if popitem() raises KeyError when dictionary is empty."""
        self.safe_dict.clear()
        self.assertTrue(len(self.safe_dict) == 0)
        with self.assertRaises(KeyError):
            self.safe_dict.popitem()

    def test_setdefault(self):
        """Test if setdefault() sets a new key or returns an existing value."""
        # 'a' already exists
        self.assertTrue(self.safe_dict.setdefault('a', 10) == 1)
        # 'z' is new
        self.assertTrue(self.safe_dict.setdefault('z', 5) == 5)

    def test_update_dict(self):
        """Test if update() correctly updates with a dictionary."""
        self.safe_dict.update({'x': 9, 'y': 8})
        self.assertTrue(self.safe_dict.get('x') == 9)
        self.assertTrue(self.safe_dict.get('y') == 8)

        self.safe_dict.update({'a': 6, 'b': 7})
        self.assertTrue(self.safe_dict['a'] == 6)
        self.assertTrue(self.safe_dict['b'] == 7)

    def test_update_kwargs(self):
        """Test if update() correctly updates with keyword arguments."""
        self.safe_dict.update(z=7, w=6)
        self.assertTrue(self.safe_dict.get('z') == 7)
        self.assertTrue(self.safe_dict.get('w') == 6)

    def test_values(self):
        """Test if values() returns dictionary values."""
        self.assertTrue(set(self.safe_dict.values()) == {1, 2, 3})

    def test_thread_safety(self):
        """Test thread safety by updating SafeDictThread from multiple threads."""
        def update_dict():
            for i in range(100):
                self.safe_dict.update({f'key_{i}': i})

        threads = [threading.Thread(target=update_dict) for _ in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        # Check if at least some keys were added
        self.assertTrue(len(self.safe_dict._data) >= 100)


if __name__ == '__main__':
    unittest.main()
