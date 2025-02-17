
# safethread/utils/__init__.py

"""
This module provides utility functions and classes.

Classes:
- **Singleton**: A class that ensures a SINGLE INSTANCE of an object is created and shared throughout the application. This is useful for managing resources or configurations that need to be globally accessible and consistent across the system.
- **Factory**: A class that provides a `create()` method to create objects dynamically based on certain parameters or configurations. This can be used for creating objects of various types at runtime, without tightly coupling the client code to specific class implementations.

Usage:
- The **Singleton** class ensures that only one instance of a class exists, making it ideal for cases like configuration managers, logging systems, or any global resource manager.
- The **Factory** class is typically used in situations where the type of object to create is determined dynamically, such as in scenarios involving dependency injection or object pools.
"""

from .Factory import Factory
from .Singleton import Singleton
