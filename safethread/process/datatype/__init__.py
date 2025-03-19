# safethread/process/datatype/__init__.py

"""
This module provides process-safe data structures to be used in multiprocess (parallel) programming scenarios.

### **Classes:**
- **ProcessRLock**: A process-safe reentrant lock (RLock) implementation.
- **ProcessSafeDict**: A process-safe dictionary implementation.
- **ProcessSafeList**: A process-safe list implementation.
- **ProcessSafeSet**: A process-safe set implementation.
- **ProcessSafeQueue**: A process-safe queue implementation.
"""

# - **AbstractProcessSafeBasicData**: A base class for process-safe basic data structures (e.g., int, float, str, bool).
# from .AbstractProcessSafeBasicData import AbstractProcessSafeBasicData
# - **ProcessSafeInt**: A process-safe int implementation.
# from .ProcessSafeInt import ProcessSafeInt

from safethread.process.datatype.ProcessRLock import ProcessRLock
from safethread.process.datatype.ProcessSafeDict import ProcessSafeDict
from safethread.process.datatype.ProcessSafeList import ProcessSafeList
from safethread.process.datatype.ProcessSafeSet import ProcessSafeSet
from safethread.process.datatype.ProcessSafeQueue import ProcessSafeQueue
# TODO
