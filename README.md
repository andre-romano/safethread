# safethread

[![PyPI](https://img.shields.io/pypi/v/safethread)](https://pypi.org/project/safethread/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](https://github.com/andre-romano/safethread/blob/main/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/safethread)](https://pypi.org/project/safethread/)

``safethread`` is a Python package that wraps common Python data structures in thread-safe / multiprocess-safe classes, providing utilities for thread-safe and multiprocess-safe operations and synchronization mechanisms (i.e., shared resources access and inter-process communication). It includes custom data structures and processing classes designed to ensure thread safety when used in multi-threaded programming, and multiprocessing safety when used in multi-processing programs.

## Features

- **Thread-Safe and Multiprocessing-Safe Data Structures**: `SafeProcessList`, `SafeProcessDict`, `SafeThreadList`, `SafeThreadDict`, `SafeThreadSet`, among others.
- **Thread and Inter-process Synchronization**: Built-in locking mechanisms to ensure safe operations in multithreaded and multiprocessing environments.
- **Threaded and Multiprocessing Classes**: Threaded and multiprocessing classes to perform parallel data processing (`Pipeline` class), scheduled function calls (`Scheduler` class), among others.
- **Utility Classes and Functions**: Additional helpers and utilities for threading  (`Pipeline`, `PipelineStageThreaded`, `SubprocessThreaded` , `Publish`/`Subscribe`, etc), for multiprocessing (`Pipeline`, `PipelineStageProcessed`, `SubprocessProcessed` etc), thread synchronization, and inter-process synchronization (IPC).

## Installation

You can install ``safethread`` from PyPI:

```bash
pip install safethread
```

## Usage

```python
from safethread.thread.datatype import SafeThreadList, SafeThreadDict
from safethread.utils import PipelineStageThreaded

# Using SafeThreadList
safe_list = SafeThreadList()
safe_list.append(1)
print(safe_list[0])  # Output: 1

# Using SafeThreadDict
safe_dict = SafeThreadDict()
safe_dict['key'] = 'value'
print(safe_dict['key'])  # Output: 'value'

# Using Pipeline (separate working thread)
stage = PipelineStageThreaded(lambda x: x * 2)
stage.start()

# Put some values into the pipeline for processing
stage.put(5)
stage.put(10)

# Get and print the results
print(f"Processed result 1: {stage.get()}")  # Output: 10 (5 * 2)
print(f"Processed result 2: {stage.get()}")  # Output: 20 (10 * 2)

# Stop pipeline
stage.stop()
stage.join()
```

For further details, check the [``examples/``](https://github.com/andre-romano/safethread/tree/master/examples) folder and the full documentation (link below).

## Documentation

The full documentation is available in [``https://andre-romano.github.io/safethread/docs``](https://andre-romano.github.io/safethread/docs)

## Contributing

We welcome contributions! If you'd like to contribute, please fork the repository and submit a pull request.

## Special thanks / Acknowledgments

- pdocs
- PyPi
- Python 3

## License and Copyright

Copyright (C) 2025 - Andre Luiz Romano Madureira

This project is licensed under the Apache License 2.0.  

For more details, see the full license text (see [``LICENSE``](https://github.com/andre-romano/safethread/blob/master/LICENSE) file).
