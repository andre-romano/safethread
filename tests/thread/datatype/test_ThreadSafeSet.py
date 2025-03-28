import unittest
import threading

from safethread.thread.datatype import ThreadSafeSet


class TestSafeThreadSet(unittest.TestCase):

    def setUp(self):
        """Create a SafeSetThread instance for testing."""
        self.safe_set = ThreadSafeSet([1, 2, 3])

    def test_initialization(self):
        safe_set = ThreadSafeSet([5, 6])
        self.assertIn(5, safe_set)

        set_custom = set([7, 8])
        safe_set = ThreadSafeSet(set_custom)
        self.assertIn(8, safe_set)

    def test_add(self):
        """Test adding elements to the set."""
        self.safe_set.add(4)
        self.assertIn(4, self.safe_set)

    def test_clear(self):
        """Test clearing the set."""
        self.safe_set.clear()
        self.assertTrue(len(self.safe_set) == 0)

    def test_difference(self):
        """Test the difference method."""
        result = self.safe_set.difference({3, 4})
        self.assertTrue(result == {1, 2})

    def test_difference_update(self):
        """Test the difference_update method."""
        self.safe_set.difference_update({3, 4})
        self.assertTrue(self.safe_set == {1, 2})

    def test_discard(self):
        """Test discarding an element."""
        self.safe_set.discard(2)
        self.assertTrue(2 not in self.safe_set)

    def test_intersection(self):
        """Test the intersection method."""
        result = self.safe_set.intersection({2, 3, 4})
        self.assertTrue(result == {2, 3})

    def test_intersection_update(self):
        """Test the intersection_update method."""
        self.safe_set.intersection_update({2, 3, 4})
        self.assertTrue(self.safe_set == {2, 3})

    def test_isdisjoint(self):
        """Test the isdisjoint method."""
        self.assertTrue(self.safe_set.isdisjoint({4, 5}))
        self.assertFalse(self.safe_set.isdisjoint({2, 5}))

    def test_issubset(self):
        """Test the issubset method."""
        self.assertTrue(self.safe_set.issubset({1, 2, 3, 4}))
        self.assertFalse(self.safe_set.issubset({4, 5}))

    def test_issuperset(self):
        """Test the issuperset method."""
        self.assertTrue(self.safe_set.issuperset({1, 2}))
        self.assertFalse(self.safe_set.issuperset({1, 4}))

    def test_pop(self):
        """Test the pop method."""
        popped_element = self.safe_set.pop()
        self.assertTrue(popped_element not in self.safe_set)

    def test_remove(self):
        """Test the remove method."""
        self.safe_set.remove(2)
        self.assertTrue(2 not in self.safe_set)
        with self.assertRaises(KeyError):
            self.safe_set.remove(5)

    def test_symmetric_difference(self):
        """Test the symmetric_difference method."""
        result = self.safe_set.symmetric_difference({2, 3, 4})
        self.assertTrue(result == {1, 4})

    def test_symmetric_difference_update(self):
        """Test the symmetric_difference_update method."""
        self.safe_set.symmetric_difference_update({2, 3, 4})
        self.assertTrue(self.safe_set == {1, 4})

    def test_union(self):
        """Test the union method."""
        result = self.safe_set.union({4, 5, 6})
        self.assertTrue(result == {1, 2, 3, 4, 5, 6})

    def test_update(self):
        """Test the update method."""
        self.safe_set.update({4, 5, 6})
        self.assertTrue(self.safe_set == {1, 2, 3, 4, 5, 6})

    def test_thread_safety(self):
        """Test thread safety by accessing the set from multiple threads."""
        def thread_func():
            for i in range(100):
                self.safe_set.add(i)
                self.safe_set.discard(i - 1)

        threads = [threading.Thread(target=thread_func) for _ in range(10)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # After all threads finish, we should have some elements in the set
        self.assertTrue(len(self.safe_set) > 0)


if __name__ == "__main__":
    unittest.main()
