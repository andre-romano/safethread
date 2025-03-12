
# safethread/utils/__init__.py

"""
This module provides utility functions and classes.

Classes:
- **Factory**: A thread-safe class that provides a `create()` method to create objects dynamically based on certain parameters or configurations. This can be used for creating objects of various types at runtime, without tightly coupling the client code to specific class implementations.
- **FileHandler**: A thread-safe asynchronous file handler that allows non-blocking reading and writing operations in a file.
- **INIFileHandler**: A thread-safe class to handle async reading and writing configuration files in INI format.    
- **Log**: A thread-safe class that provides a simple interface for logging messages to the console and/or a log file.
- **Pipeline**: A thread-safe class that connects multiple ``utils.PipelineStage`` objects together (input_queue => Pipe 1 => Pipe 2 => ... => output_queue).
- **PipelineStage**: A thread-safe class that runs threads to processes data (using a Callable) from an Input Queue and places its output in an Output Queue.
- **Publisher**: A thread-safe class that maintains a list of Subscriber instances and notifies them when data changes.    
- **Singleton**: A thread-safe class that ensures a SINGLE INSTANCE of an object is created and shared throughout the application. This is useful for managing resources or configurations that need to be globally accessible and consistent across the system.    
- **Subscriber**: A thread-safe class that subscribes to a Publisher and receives notifications when data changes.
"""

from .Factory import Factory
from .FileHandler import FileHandler
from .INIFileHandler import INIFileHandler
from .Log import Log
from .Pipeline import Pipeline
from .PipelineStage import PipelineStage
from .Publisher import Publisher
from .Singleton import Singleton
from .Subscriber import Subscriber
from .utils import *
