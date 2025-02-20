
# safethread/utils/__init__.py

"""
This module provides threaded classes.

Classes:
- **Scheduler**: A class that runs a scheduled Callable (function, lambda, etc), after a pre-defined timeout, either singleshot or periodically.
- **Subprocess**: A class that runs a subprocess within a separate thread.
- **ThreadBase**: An abstract class manages threads.
"""

from .Scheduler import Scheduler
from .Subprocess import Subprocess
from .ThreadBase import ThreadBase
