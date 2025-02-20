
# safethread/utils/__init__.py

"""
This module provides utility functions and classes.

Classes:
- **Factory**: A class that provides a `create()` method to create objects dynamically based on certain parameters or configurations. This can be used for creating objects of various types at runtime, without tightly coupling the client code to specific class implementations.
- **Pipeline**: A class that connects multiple ``thread.PipelineStage`` objects together (input_queue => Pipe 1 => Pipe 2 => ... => output_queue).
- **PipelineStage**: A class that runs threads to processes data (using a Callable) from an Input Queue and places its output in an Output Queue.
- **Singleton**: A class that ensures a SINGLE INSTANCE of an object is created and shared throughout the application. This is useful for managing resources or configurations that need to be globally accessible and consistent across the system.
- **utils**: A file containing utility functions for the library.
"""

from .Factory import Factory
from .Pipeline import Pipeline
from .PipelineStage import PipelineStage
from .Singleton import Singleton
from .utils import *
