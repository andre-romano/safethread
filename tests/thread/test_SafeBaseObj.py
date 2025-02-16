
import unittest

import threading

# Adjust the import path as needed
from safethread.thread import SafeBaseObj


class TestSafeBaseObj(unittest.TestCase):
    def setUp(self):
        """Initialize test objects before each test."""
        self.obj = SafeBaseObj(10)
        self.obj_float1 = SafeBaseObj(10.2)
        self.obj_float2 = SafeBaseObj(10.7)

        self.obj_bool = SafeBaseObj(True)

        self.obj_list = SafeBaseObj([1, 2, 3, 4])
        self.obj_set = SafeBaseObj({1, 2, 3, 4})
        self.obj_dict = SafeBaseObj({
            'a': 'A',
            'b': 'B',
            'c': 'C',
            'd': 'D'
        })

    def test_index(self):
        """Test the __index__ method."""
        self.assertEqual(self.obj.__index__(), 10)

    def test_ceil(self):
        """Test the __ceil__ method."""
        self.assertEqual(self.obj.__ceil__(), 10)
        self.assertEqual(self.obj_float1.__ceil__(), 11)
        self.assertEqual(self.obj_float2.__ceil__(), 11)

    def test_floor(self):
        """Test the __floor__ method."""
        self.assertEqual(self.obj.__floor__(), 10)
        self.assertEqual(self.obj_float1.__floor__(), 10)
        self.assertEqual(self.obj_float2.__floor__(), 10)

    def test_trunc(self):
        """Test the __trunc__ method."""
        self.assertEqual(self.obj.__trunc__(), 10)
        self.assertEqual(self.obj_float1.__trunc__(), 10)
        self.assertEqual(self.obj_float2.__trunc__(), 10)

    def test_round(self):
        """Test the __round__ method."""
        self.assertEqual(self.obj_float1.__round__(), 10)
        self.assertEqual(self.obj_float2.__round__(), 11)

        self.assertEqual(self.obj_float1.__round__(1), 10.2)
        self.assertEqual(self.obj_float2.__round__(1), 10.7)

    def test_divmod(self):
        """Test the __divmod__ method."""
        self.assertEqual(self.obj.__divmod__(3), (3, 1))

    def test_iadd(self):
        """Test the __iadd__ method."""
        self.obj.__iadd__(5)
        self.assertEqual(self.obj._data, 15)

    def test_math_operations(self):
        """Test addition, subtraction, multiplication, division, etc."""
        self.assertEqual((self.obj + 5)._data, 15)
        self.assertEqual((self.obj - 3)._data, 7)
        self.assertEqual((self.obj * 2)._data, 20)
        self.assertEqual((self.obj / 2)._data, 5.0)
        self.assertEqual((self.obj // 3)._data, 3)
        self.assertEqual((self.obj % 3)._data, 1)
        self.assertEqual((self.obj ** 2)._data, 100)

    def test_bitwise_operations(self):
        """Test bitwise operations."""
        self.assertEqual((self.obj << 1)._data, 20)
        self.assertEqual((self.obj >> 1)._data, 5)
        self.assertEqual((self.obj & 0b0110)._data, 2)
        self.assertEqual((self.obj | 0b0001)._data, 11)
        self.assertEqual((self.obj ^ 0b0011)._data, 9)

    def test_reverse_operations(self):
        """Test reverse arithmetic operations."""
        self.assertEqual((5 + self.obj)._data, 15)
        self.assertEqual((20 - self.obj)._data, 10)
        self.assertEqual((3 * self.obj)._data, 30)
        self.assertEqual((20 / self.obj)._data, 2.0)
        self.assertEqual((30 // self.obj)._data, 3)
        self.assertEqual((30 % self.obj)._data, 0)
        self.assertEqual((2 ** self.obj)._data, 1024)

    def test_reverse_bitwise_operations(self):
        """Test reverse bitwise operations."""
        self.assertEqual((1 << self.obj)._data, 1024)
        self.assertEqual((40 >> self.obj)._data, 0)
        self.assertEqual((5 & self.obj)._data, 0)
        self.assertEqual((5 | self.obj)._data, 15)
        self.assertEqual((5 ^ self.obj)._data, 15)

    def test_abs_neg_pos_invert(self):
        """Test absolute, negation, positive, and inversion."""
        self.assertEqual(abs(self.obj)._data, 10)
        self.assertEqual(abs(-self.obj)._data, 10)

        self.assertEqual((-self.obj)._data, -10)
        self.assertEqual((+self.obj)._data, 10)
        self.assertEqual((~self.obj)._data, -11)

    def test_comparisons(self):
        """Test comparison operators."""
        self.assertTrue(self.obj != 5)
        self.assertTrue(self.obj == 10)
        self.assertTrue(self.obj == self.obj)

        self.assertTrue(self.obj <= 11)
        self.assertTrue(self.obj <= 10)
        self.assertFalse(self.obj <= 9)

        self.assertFalse(self.obj >= 11)
        self.assertTrue(self.obj >= 10)
        self.assertTrue(self.obj >= 9)

        self.assertTrue(self.obj < 15)
        self.assertTrue(self.obj > 5)

    def test_index_operations(self):
        """Test index-based operations."""
        self.assertEqual(self.obj_list[2], 3)
        self.assertEqual(self.obj_dict['d'], 'D')

        self.obj_list[1] = 42
        self.assertEqual(self.obj_list[1], 42)

        del self.obj_list[3]
        with self.assertRaises(IndexError):
            _ = self.obj_list[3]

        with self.assertRaises(Exception):
            del self.obj_set[3]

    def test_contains(self):
        """Test the __contains__ method."""
        self.assertTrue(2 in self.obj_list)
        self.assertFalse(10 in self.obj_list)

        self.assertFalse(15 in self.obj_set)

        self.assertTrue('a' in self.obj_dict)

    def test_size_methods(self):
        """Test __sizeof__ and __len__ methods."""
        self.assertEqual(len(self.obj_list), 4)
        self.assertGreater(self.obj_list.__sizeof__(), 0)

    def test_iter(self):
        """Test __iter__ method."""
        self.assertEqual(list(iter(self.obj_list)), [1, 2, 3, 4])

    def test_hash(self):
        """Test __hash__ method."""
        self.assertIsInstance(hash(self.obj), int)

        self.assertEqual(hash(self.obj), 10)

    def test_repr_str(self):
        """Test __repr__ and __str__ methods."""
        self.assertEqual(repr(self.obj), "10")
        self.assertEqual(str(self.obj), "10")

        self.assertEqual(str(self.obj_list), '[1, 2, 3, 4]')

    def test_bool(self):
        """Test __bool__ method."""
        self.assertTrue(bool(self.obj_bool))

        self.assertFalse(bool(SafeBaseObj(0)))

    def test_type_conversions(self):
        """Test __int__, __float__ methods."""
        self.assertEqual(int(self.obj), 10)
        self.assertEqual(float(self.obj), 10.0)

        self.assertEqual(int(self.obj_float1), 10)
        self.assertEqual(int(self.obj_float2), 10)

    def test_copy_methods(self):
        """Test copy and copyObj methods."""
        copied_obj = self.obj_list.copy()
        self.assertEqual(copied_obj, self.obj_list)
        self.assertNotEqual(id(copied_obj), id(self.obj_list))

        copied_internal = self.obj_list.copyObj()
        self.assertEqual(copied_internal, self.obj_list._data)

    def test_thread_safety(self):
        """Test that multiple threads can access SafeBaseObj safely."""
        initial_value = self.obj._data
        n_iterations = 1000
        n_threads = 10

        def increment():
            for _ in range(n_iterations):
                with self.obj._lock:
                    self.obj._data += 1

        threads = [threading.Thread(target=increment)
                   for _ in range(n_threads)]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(self.obj._data,
                         initial_value + (n_iterations * n_threads))

    def test_thread_safety_internal(self):
        """Test that multiple threads can access SafeBaseObj safely."""
        initial_value = self.obj._data
        n_iterations = 1000
        n_threads = 10

        def increment():
            obj2 = SafeBaseObj(1)
            for _ in range(n_iterations):
                self.obj += obj2

        threads = [threading.Thread(target=increment)
                   for _ in range(n_threads)]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(self.obj._data,
                         initial_value + (n_iterations * n_threads))


if __name__ == '__main__':
    unittest.main()
