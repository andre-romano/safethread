# safethread

[![PyPI](https://img.shields.io/pypi/v/safethread)](https://pypi.org/project/safethread/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](https://github.com/andre-romano/safethread/blob/main/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/safethread)](https://pypi.org/project/safethread/)

``safethread`` is a Python package that wraps common Python data structures in thread-safe classes, providing utilities for thread-safe operations and synchronization mechanisms. It includes custom data structures designed to ensure thread safety when used in multi-threaded programming.

## Features

- **Thread-Safe Data Structures**: `SafeList`, `SafeDict`, `SafeTuple`, `SafeSet`, among others.
- **Thread Synchronization**: Built-in locking mechanisms to ensure safe operations in multithreaded environments.
- **Threaded Classes**: Threaded classes to perform parallel data processing, scheduled function calls, among others.
- **Utility Classes and Functions**: Additional helpers and utilities for threading  (`Pipeline`, `PipelineStage`, `Publish`/`Subscribe`, etc), synchronization and other functionality unrelated to multithread programming.

## Installation

You can install ``safethread`` from PyPI:

```bash
pip install safethread
```

## Usage

```python
from safethread.datatype import SafeList, SafeDict
from safethread.utils import PipelineStage

# Using SafeList
safe_list = SafeList()
safe_list.append(1)
print(safe_list[0])  # Output: 1

# Using SafeDict
safe_dict = SafeDict()
safe_dict['key'] = 'value'
print(safe_dict['key'])  # Output: 'value'

# Using Pipeline (separate working thread)
stage = PipelineStage(lambda x: x * 2)
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

For further details, check the [``examples/``](./examples/) folder and the full documentation (link below).

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

For more details, see the full license text (see [``LICENSE``](./LICENSE) file).
