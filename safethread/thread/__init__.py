
# safethread/thread/__init__.py

"""
This module provides threaded classes, that inherit from ThreadBase. It also contains `.datatype` module, that contain thread-safe data structures.

> Warning: This module supports multithreading in Python (concurrent programming), not parallel processing (multithreading in Python is implemented using userspace threads, due to Python's garbage collector limitation). If you need true paralellism, you'll need to create multiple Python processes (multiprocessing). In that case, check `safethread.process` module.

Classes:
- **SchedulerThread**: A thread-safe class that runs a scheduled Callable (function, lambda, etc), after a pre-defined timeout, either singleshot or periodically.
- **SubprocessThread**: A thread-safe class that runs a subprocess within a separate thread.
- **ThreadBase**: An abstract class manages threads.
"""

from .SchedulerThread import SchedulerThread
from .SubprocessThread import SubprocessThread
from .ThreadBase import ThreadBase
