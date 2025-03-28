
# safethread/thread/utils/__init__.py

"""
This module provides thread-safe utility functions and classes.

Classes:
- **ThreadFileHandler**: A thread-safe asynchronous file handler that allows non-blocking reading and writing operations in a file.
- **ThreadINIFileHandler**: A thread-safe class to handle async reading and writing configuration files in INI format.    
- **ThreadLog**: A thread-safe class that provides a simple interface for logging messages to the console and/or a log file.
- **ThreadPipeline**: A thread-safe class that connects multiple ``utils.PipelineStage`` objects together (input_queue => Pipe 1 => Pipe 2 => ... => output_queue).
- **ThreadPipelineStage**: A thread-safe class that runs threads to manipulate data (using a Callable) from an Input Queue and places its output in an Output Queue.
- **ThreadPublisher**: A thread-safe class that maintains a list of Subscriber instances and notifies them when data changes.    
- **ThreadSingleton**: A thread-safe class that ensures a SINGLE INSTANCE of an object is created and shared throughout the application. This is useful for managing resources or configurations that need to be globally accessible and consistent across the system.    
- **ThreadSubscriber**: A thread-safe class that subscribes to a Publisher and receives notifications when data changes.
"""

from safethread.thread.utils.ThreadFileHandler import ThreadFileHandler
from safethread.thread.utils.ThreadINIFileHandler import ThreadINIFileHandler
from safethread.thread.utils.ThreadLog import ThreadLog
from safethread.thread.utils.ThreadPipeline import ThreadPipeline
from safethread.thread.utils.ThreadPipelineStage import ThreadPipelineStage
from safethread.thread.utils.ThreadPublisher import ThreadPublisher
from safethread.thread.utils.ThreadSingleton import ThreadSingleton
from safethread.thread.utils.ThreadSubscriber import ThreadSubscriber
