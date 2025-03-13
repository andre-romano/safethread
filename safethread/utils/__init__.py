
# safethread/utils/__init__.py

"""
This module provides utility functions and classes that are simultaneously thread-safe and multiprocess-safe, to be used in hybrid scenarios that contain multithreaded (concurrent) and multiprocessing (parallel) code.

Classes:
- **Factory**: A thread-safe class that provides a `create()` method to create objects dynamically based on certain parameters or configurations. This can be used for creating objects of various types at runtime, without tightly coupling the client code to specific class implementations.
- **Regex**: A thread-safe class that performs common regex operations such as matching, searching, and replacing patterns in strings, while ensuring thread safety.
"""

from .Factory import Factory
from .Regex import Regex
from .utils import *
