
# safethread/utils/__init__.py

"""
This module provides threaded classes.

Classes:
- **Pipeline**: A class that runs a thread, that reads an Input Queue and places its output in an Output Queue.
- **Subprocess**: A class that runs a subprocess within a separate thread.
- **ThreadBase**: An abstract class manages threads.
"""

from .Pipeline import Pipeline
from .Subprocess import Subprocess
from .ThreadBase import ThreadBase
