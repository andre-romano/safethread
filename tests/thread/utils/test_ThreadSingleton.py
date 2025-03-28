import unittest

# Adjust the import path as needed
from safethread.thread.utils import ThreadSingleton


# Sample subclass to test Singleton behavior
class SingletonSubclass(ThreadSingleton):
    def __init__(self, value: int):
        super().__init__()
        self.value = value

# Sample subclass to test Singleton behavior


class SingletonSubclassTwo(ThreadSingleton):
    def __init__(self):
        super().__init__()


class TestThreadSingleton(unittest.TestCase):
    def setUp(self):
        """Setup method to run before each test."""
        self.obj1 = SingletonSubclass.get_instance(10)
        self.obj2 = SingletonSubclass.get_instance(20)

        self.obj3 = SingletonSubclassTwo.get_instance()
        self.obj4 = SingletonSubclassTwo.get_instance()

    def test_singleton_creation(self):
        """Test that the Singleton class only creates one instance."""

        # Assert that both self.obj1 and self.obj2 are the same instance
        self.assertIs(self.obj1, self.obj2,
                      "Singleton instances are not the same!")
        self.assertIs(self.obj3, self.obj4,
                      "SingletonTwo instances are not the same!")

        # Assert that the value remains the same (due to singleton pattern)
        self.assertTrue(
            self.obj1.value == 10, f"Singleton value '{self.obj1.value}' was not retained properly")

    def test_singleton_instance_reuse(self):
        """Test that the Singleton class reuses the instance."""
        self.obj1 = SingletonSubclass.get_instance(5)
        self.obj2 = SingletonSubclass.get_instance(30)

        # Assert that the instance is the same
        self.assertIs(self.obj1, self.obj2,
                      "Singleton should reuse the same instance!")

        # Assert that the value should not change (should remain as 10)
        self.assertTrue(
            self.obj1.value == 10, "Singleton value was not retained correctly across multiple calls")

    def test_singleton_same_atributes(self):
        # Assert that the value remains as 2 (the first instance's value)
        self.obj2.value = 2
        self.assertTrue(
            self.obj1.value == 2, "Singleton value was not set properly")


if __name__ == '__main__':
    unittest.main()
