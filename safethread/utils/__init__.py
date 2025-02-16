
# safethread/utils/__init__.py

"""
safetheread.utils

This package provides utilities for handling threading and concurrency safely in Python.
It uses threading module primitives to do so.

If you intent to use Python Processes, you will need Inter-Process Communication (IPC) synchronization. 
In that case, check safethread.process package.
"""

from .Factory import Factory
from .Singleton import Singleton
