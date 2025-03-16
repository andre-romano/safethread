
# safethread/process/utils/__init__.py

"""
This module provides process-safe utility functions and classes.

Classes:
- **PipelineProcessed**: A process-safe class that connects multiple ``utils.PipelineStageProcessed`` objects together (input_queue => Pipe 1 => Pipe 2 => ... => output_queue).
- **PipelineStageProcessed**: A process-safe class that runs processes to manipulate data (using a Callable) from an Input Queue and places its output in an Output Queue.
"""

# TODO
# from .PipelineProcessed import PipelineProcessed
# from .PipelineStageProcessed import PipelineStageProcessed
