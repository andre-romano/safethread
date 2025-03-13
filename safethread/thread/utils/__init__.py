
# safethread/thread/utils/__init__.py

"""
This module provides thread-safe utility functions and classes.

Classes:
- **FileHandler**: A thread-safe asynchronous file handler that allows non-blocking reading and writing operations in a file.
- **INIFileHandler**: A thread-safe class to handle async reading and writing configuration files in INI format.    
- **Log**: A thread-safe class that provides a simple interface for logging messages to the console and/or a log file.
- **Pipeline**: A thread-safe class that connects multiple ``utils.PipelineStage`` objects together (input_queue => Pipe 1 => Pipe 2 => ... => output_queue).
- **PipelineStageThreaded**: A thread-safe class that runs threads to manipulate data (using a Callable) from an Input Queue and places its output in an Output Queue.
- **Publisher**: A thread-safe class that maintains a list of Subscriber instances and notifies them when data changes.    
- **Singleton**: A thread-safe class that ensures a SINGLE INSTANCE of an object is created and shared throughout the application. This is useful for managing resources or configurations that need to be globally accessible and consistent across the system.    
- **Subscriber**: A thread-safe class that subscribes to a Publisher and receives notifications when data changes.
"""

from .FileHandler import FileHandler
from .INIFileHandler import INIFileHandler
from .Log import Log
from .Pipeline import Pipeline
from .PipelineStageThreaded import PipelineStageThreaded
from .Publisher import Publisher
from .Singleton import Singleton
from .Subscriber import Subscriber
