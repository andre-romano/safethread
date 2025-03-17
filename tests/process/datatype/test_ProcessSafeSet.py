import multiprocessing
import unittest
from safethread.process.datatype import ProcessSafeSet


def worker(safe_set: ProcessSafeSet, value):
    safe_set.add(value)


class TestProcessSafeSet(unittest.TestCase):

    def test_initialization(self):
        data = {1, 2, 3}
        safe_set = ProcessSafeSet(data)
        self.assertTrue(safe_set == data)

        data = [1, 2, 3]
        safe_set = ProcessSafeSet(data)
        safe_set_two = ProcessSafeSet(data)
        self.assertTrue(safe_set == data)
        self.assertTrue(safe_set == set(data))
        self.assertTrue(safe_set == safe_set_two)

        safe_set = ProcessSafeSet(safe_set)
        self.assertTrue(safe_set == data)

        safe_set = ProcessSafeSet()
        self.assertTrue(safe_set == [])

    def test_add(self):
        safe_set = ProcessSafeSet({1, 2, 3})
        safe_set.add(4)
        self.assertIn(4, safe_set._data)

    def test_clear(self):
        safe_set = ProcessSafeSet({1, 2, 3})
        safe_set.clear()
        self.assertTrue(len(safe_set._data) == 0)

    def test_difference(self):
        safe_set = ProcessSafeSet({1, 2, 3})
        result = safe_set.difference({2, 3})
        self.assertTrue(result == {1})

    def test_difference_update(self):
        safe_set = ProcessSafeSet({1, 2, 3})
        safe_set.difference_update({2, 3})
        self.assertTrue(safe_set._data == {1})

    def test_discard(self):
        safe_set = ProcessSafeSet({1, 2, 3})
        safe_set.discard(2)
        self.assertTrue(2 not in safe_set._data)

    def test_intersection(self):
        safe_set = ProcessSafeSet({1, 2, 3})
        result = safe_set.intersection({2, 3, 4})
        self.assertTrue(result == {2, 3})

    def test_intersection_update(self):
        safe_set = ProcessSafeSet({1, 2, 3})
        safe_set.intersection_update({2, 3, 4})
        self.assertTrue(safe_set == {2, 3})

    def test_isdisjoint(self):
        safe_set = ProcessSafeSet({1, 2, 3})
        self.assertTrue(safe_set.isdisjoint({4, 5}))
        self.assertFalse(safe_set.isdisjoint({1}))

    def test_issubset(self):
        safe_set = ProcessSafeSet({1, 2, 3})
        self.assertTrue(safe_set.issubset({1, 2, 3, 4}))

    def test_issuperset(self):
        safe_set = ProcessSafeSet({1, 2, 3})
        self.assertTrue(safe_set.issuperset({1, 2}))

    def test_pop(self):
        safe_set = ProcessSafeSet({1, 2, 3})
        value = safe_set.pop()
        self.assertTrue(value not in safe_set._data)

    def test_remove(self):
        safe_set = ProcessSafeSet({1, 2, 3})
        safe_set.remove(3)
        self.assertTrue(3 not in safe_set._data)

    def test_symmetric_difference(self):
        safe_set = ProcessSafeSet({1, 2, 3})
        result = safe_set.symmetric_difference({2, 4})
        self.assertTrue(result == {1, 3, 4})

    def test_symmetric_difference_update(self):
        safe_set = ProcessSafeSet({1, 2, 3})
        safe_set.symmetric_difference_update({2, 4})
        self.assertTrue(safe_set._data == {1, 3, 4})

    def test_union(self):
        safe_set = ProcessSafeSet({1, 2, 3})
        result = safe_set.union({4, 5})
        self.assertTrue(result == {1, 2, 3, 4, 5})

    def test_update(self):
        safe_set = ProcessSafeSet({1, 2, 3})
        safe_set.update({4, 5})
        self.assertTrue(safe_set == {1, 2, 3, 4, 5})

    def test_thread_safety(self):
        safe_set = ProcessSafeSet({1, 2, 3})

        processes = [
            multiprocessing.Process(
                target=worker, args=(safe_set, i)
            ) for i in range(10, 20)]
        for p in processes:
            p.start()
        for p in processes:
            p.join()

        for i in range(10, 20):
            self.assertIn(i, safe_set._data)


if __name__ == '__main__':
    unittest.main()
