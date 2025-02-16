
# safethread/thread/__init__.py

"""
safetheread.thread

This package provides utilities for handling threading and concurrency safely in Python.
It uses threading module primitives to do so.

If you intent to use Python Processes, you will need Inter-Process Communication (IPC) synchronization. 
In that case, check safethread.process package.
"""

from .SafeBaseObj import SafeBaseObj
from .SafeDict import SafeDict
from .SafeList import SafeList
