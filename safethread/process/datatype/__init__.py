# safethread/process/datatype/__init__.py

"""
This module provides process-safe data structures to be used in multiprocess (parallel) programming scenarios.

### **Classes:**
- **ProcessRLock**: A process-safe reentrant lock (RLock) implementation.
- **ProcessSafeDict**: A process-safe dictionary implementation.
- **ProcessSafeList**: A process-safe list implementation.
- **ProcessSafeQueue**: A process-safe queue implementation.
"""

from .ProcessRLock import ProcessRLock
from .ProcessSafeDict import ProcessSafeDict
# TODO
