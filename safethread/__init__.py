# safethread/__init__.py

"""
The `safethread` package provides a collection of thread-safe utilities for managing data structures and synchronization in multi-threaded environments.

The package is designed to ensure safe, concurrent operations on common Python data structures such as lists, dictionaries among others.

### **Modules:**
- **thread**: Provides thread-safe classes for multi-threaded programming like `SubprocessThread` and `BaseThread`.
    - **thread.datatype**: Provides thread-safe data structures like `SafeThreadList` and `SafeThreadDict`.
    - **thread.utils**: Offers thread-safe utility functions and classes.
- **process**: Provides process-safe classes for multi-process programming like `SubprocessProcess` and `BaseProcess`.
    - **process.datatype**: Provides process-safe data structures like `SafeProcessList` and `SafeProcessDict`.
    - **process.utils**: Offers process-safe utility functions and classes.
- **utils**: Offers utility functions and classes that are simultaneously thread-safe and process-safe (for multithreaded and multiprocessing programming).

### **Features:**
- **Thread-Safe and Multiprocessing-Safe Data Structures**: Safe implementations of common data structures (list, dict) to avoid race conditions in concurrent threads and parallel processes.
- **Thread / Multiprocess Synchronization**: Use of Python's `threading.RLock` and `multiprocessing.RLock` to manage concurrent access to shared resources, and inter-process communication (IPC).
- **Threaded / Multiprocessed Classes**: Threaded and multiprocessed classes to perform parallel data processing , scheduled function calls (`SchedulerThread`), among others.
- **Utility Classes**: Additional helpers and utilities for threading (`Pipeline`, `PipelineStageThreaded`, `Publish`/`Subscribe`, etc), multiprocessing (`Pipeline`, `PipelineStageProcessed`, etc), and thread/process synchronization.

### **Installation:**
- Install via PyPI: `pip install safethread`
- Clone the repository for local development: `git clone https://github.com/andre-romano/safethread.git`

### **License:**
- Apache-2.0 License
"""

from .AbstractContext import AbstractContext
from .AbstractEvent import AbstractEvent
from .AbstractLock import AbstractLock
from .AbstractParallel import AbstractParallel
from .AbstractPicklable import AbstractPicklable
from .AbstractProcess import AbstractProcess
from .AbstractScheduler import AbstractScheduler
from .AbstractSubprocess import AbstractSubprocess
