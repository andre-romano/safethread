# safethread/datatype/__init__.py

"""
This module provides data structures that are simultaneously thread-safe and multiprocess-safe, to be used in hybrid scenarios that contain multithreaded (concurrent) and multiprocessing (parallel) code.

### **Classes:**
- **AbstractSafeBase**: A base class for creating thread-safe or multiprocess-safe data structures.
- **AbstractSafeDict**: A base dictionary-like data structure to create thread-safe or multiprocess-safe implementations.
- **AbstractSafeList**: A base list-like data structure to create thread-safe or multiprocess-safe implementations.
- **AbstractSafeQueue**: A base queue-like data structure to create thread-safe or multiprocess-safe implementations.
- **AbstractSafeSet**: A base set-like data structure to create thread-safe or multiprocess-safe implementations.
"""

from safethread.datatype.AbstractSafeBase import AbstractSafeBase
from safethread.datatype.AbstractSafeDict import AbstractSafeDict
from safethread.datatype.AbstractSafeList import AbstractSafeList
from safethread.datatype.AbstractSafeQueue import AbstractSafeQueue
from safethread.datatype.AbstractSafeSet import AbstractSafeSet
