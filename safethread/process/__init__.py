
# safethread/process/__init__.py

"""
This module provides multiprocessed classes, that inherit from BaseProcess. It also contains `.datatype` module, that contain process-safe data structures.

> Warning: This module requires that data exchanged between Python be pickable (serializable). Examples of pickable structures are global functions, simple immutable data types (int, str, bool), data structures provided by ``.datatype`` module or by `multiprocessing.Manager()`. 

Classes:
- **BaseProcess**: An process-safe class that manages processes safely.
- **ProcessEvent**: An process-safe class that manages processes events safely.
- **SchedulerProcess**: A process-safe class that runs a scheduled global Callable function after a pre-defined timeout, either singleshot or periodically.
- **SubprocessProcess**: A process-safe class that runs a subprocess within a separate process.
"""

from .BaseProcess import BaseProcess
from .ProcessEvent import ProcessEvent
# from .SchedulerProcess import SchedulerProcess
# from .SubprocessProcess import SubprocessProcess
