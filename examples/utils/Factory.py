from typing import Self

from safethread.utils import Factory


class MyClass(Factory):
    def __init__(self, name: str):
        self.name = name

    def greet(self):
        return f"Hello, {self.name}!"


# Using the factory method to create instances of MyClass
instance = MyClass.create("Alice")
print(instance.greet())  # Output: Hello, Alice!

# You can also subclass Factory and use create() in the same way


class AnotherClass(Factory):
    def __init__(self, value: int):
        self.value = value

    def double(self):
        return self.value * 2


another_instance = AnotherClass.create(5)
print(another_instance.double())  # Output: 10
