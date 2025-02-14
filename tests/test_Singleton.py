import unittest

# Adjust the import path as needed
from safethread.utils import Singleton


# Sample subclass to test Singleton behavior
class SingletonSubclass(Singleton):
    def __init__(self, value: int):
        self.value = value

# Sample subclass to test Singleton behavior


class SingletonSubclassTwo(Singleton):
    def __init__(self):
        pass


class TestSingleton(unittest.TestCase):
    def setUp(self):
        """Setup method to run before each test."""
        self.obj1 = SingletonSubclass.getInstance(10)
        self.obj2 = SingletonSubclass.getInstance(20)

        self.obj3 = SingletonSubclassTwo.getInstance()
        self.obj4 = SingletonSubclassTwo.getInstance()

    def test_singleton_creation(self):
        """Test that the Singleton class only creates one instance."""

        # Assert that both self.obj1 and self.obj2 are the same instance
        self.assertIs(self.obj1, self.obj2,
                      "Singleton instances are not the same!")
        self.assertIs(self.obj3, self.obj4,
                      "SingletonTwo instances are not the same!")

        # Assert that the value remains the same (due to singleton pattern)
        self.assertEqual(
            self.obj1.value, 10, f"Singleton value '{self.obj1.value}' was not retained properly")

    def test_singleton_instance_reuse(self):
        """Test that the Singleton class reuses the instance."""
        self.obj1 = SingletonSubclass.getInstance(5)
        self.obj2 = SingletonSubclass.getInstance(30)

        # Assert that the instance is the same
        self.assertIs(self.obj1, self.obj2,
                      "Singleton should reuse the same instance!")

        # Assert that the value should not change (should remain as 10)
        self.assertEqual(
            self.obj1.value, 10, "Singleton value was not retained correctly across multiple calls")

    def test_singleton_same_atributes(self):
        # Assert that the value remains as 2 (the first instance's value)
        self.obj2.value = 2
        self.assertEqual(
            self.obj1.value, 2, "Singleton value was not set properly")


if __name__ == '__main__':
    unittest.main()
