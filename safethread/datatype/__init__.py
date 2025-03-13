# safethread/datatype/__init__.py

"""
This module provides data structures that are simultaneously thread-safe and multiprocess-safe, to be used in hybrid scenarios that contain multithreaded (concurrent) and multiprocessing (parallel) code.

### **Classes:**
- **HybridRLock**: A thread and process-safe lock class that supports both inter-process (multiprocessing) and intra-process (threading) synchronization.
"""

from .HybridRLock import HybridRLock
