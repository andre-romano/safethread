# safethread/__init__.py

"""
The `safethread` package provides a collection of thread-safe utilities for managing data structures and synchronization in multi-threaded environments.

The package is designed to ensure safe, concurrent operations on common Python data structures such as lists, dictionaries among others.

### **Modules:**
- **thread**: Provides thread-safe classes for multi-threaded programming like `SubprocessThread`.
    - **thread.datatype**: Provides thread-safe data structures like `SafeList` and `SafeDict`.
- **utils**: Offers utility functions and classes for multithreaded and multiprocessing programming.

### **Features:**
- **Thread-Safe and Multiprocessing-Safe Data Structures**: Safe implementations of common data structures (list, dict) to avoid race conditions in concurrent threads and parallel processes.
- **Thread / Multiprocess Synchronization**: Use of Python's `threading.RLock` and `multiprocessing.RLock` to manage concurrent access to shared resources, and inter-process communication (IPC).
- **Threaded / Multiprocessed Classes**: Threaded and multiprocessed classes to perform parallel data processing , scheduled function calls (`SchedulerThread`), among others.
- **Utility Classes**: Additional helpers and utilities for threading (`Pipeline`, `PipelineStageThread`, `Publish`/`Subscribe`, etc), multiprocessing (`Pipeline`, `PipelineStageProcess`, etc), and thread/process synchronization.

### **Installation:**
- Install via PyPI: `pip install safethread`
- Clone the repository for local development: `git clone https://github.com/andre-romano/safethread.git`

### **License:**
- Apache-2.0 License
"""
