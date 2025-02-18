
# safethread/utils/__init__.py

"""
This module provides threaded classes.

Classes:
- **Pipeline**: A class that runs a thread, that reads an Input Queue and places its output in an Output Queue.
- **Scheduler**: A class that runs a scheduled Callable (function, lambda, etc), after a pre-defined timeout, either singleshot or periodically.
- **Subprocess**: A class that runs a subprocess within a separate thread.
- **ThreadBase**: An abstract class manages threads.
"""

from .Pipeline import Pipeline
from .Scheduler import Scheduler
from .Subprocess import Subprocess
from .ThreadBase import ThreadBase
