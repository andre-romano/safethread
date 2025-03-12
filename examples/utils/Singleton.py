
from safethread.utils import Singleton


class MyClass(Singleton):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"MyClass instance with value: {self.value}"


# Get the first instance of MyClass
instance1 = MyClass.get_instance(10)
print(instance1)  # Output: MyClass instance with value: 10

# Try to create a second instance with a different value
instance2 = MyClass.get_instance(20)
print(instance2)  # Output: MyClass instance with value: 10

# Verify that both instances are the same (singleton behavior)
print(instance1 is instance2)  # Output: True
