
# safethread/thread/__init__.py

"""
This module provides classes and utilities for thread synchronization, as well as thread-safe data structures to be used in concurrent programming scenarios.

Classes:
- **SafeList**: A thread-safe list implementation that ensures safe operations on the list by using locking mechanisms. Methods include `append`, `clear`, `pop`, and `sort`.
- **SafeDict**: A thread-safe dictionary implementation that provides thread-safe methods like `get`, `pop`, `setdefault`, and `update` to avoid race conditions.
"""

from .SafeBaseObj import SafeBaseObj
from .SafeDict import SafeDict
from .SafeList import SafeList
