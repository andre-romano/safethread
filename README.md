# safethread

[![PyPI](https://img.shields.io/pypi/v/safethread)](https://pypi.org/project/safethread/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](https://github.com/andre-romano/safethread/blob/main/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/safethread)](https://pypi.org/project/safethread/)

``safethread`` is a Python package that wraps common Python data structures in thread-safe classes, providing utilities for thread-safe operations and synchronization mechanisms. It includes custom data structures designed to ensure thread safety when used in multi-threaded programming.

## Features

- **Thread-Safe Data Structures**: `SafeList`, `SafeDict`, `SafeTuple`, `SafeSet`, among others.
- **Thread Synchronization**: Built-in locking mechanisms to ensure safe operations in multithreaded environments.
- **Utility Methods**: Additional helpers and utilities for threading and synchronization.

## Installation

You can install ``safethread`` from PyPI:

```bash
pip install safethread
```

## Usage

```python
from safethread.thread import SafeList, SafeDict, SafeTuple, SafeSet, SafeQueue

# Using SafeList
safe_list = SafeList()
safe_list.append(1)
print(safe_list[0])  # Output: 1

# Using SafeDict
safe_dict = SafeDict()
safe_dict['key'] = 'value'
print(safe_dict['key'])  # Output: 'value'

# Using SafeTuple
safe_tuple = SafeTuple(('a','b'))
print(safe_tuple[0])  # Output: 'a'

# Using SafeSet
safe_set = SafeSet(['x','y'])
safe_set.add('z')
print('z' in safe_set)  # Output: True

# Using SafeQueue
safe_queue = SafeQueue()
safe_queue.put(55)
print(safe_queue.get())  # Output: 55
```

For further details, check the full documentation (link below) and [``tests/``](./tests/) folder.

## Documentation

The full documentation is available in [``https://andre-romano.github.io/safethread/docs``](https://andre-romano.github.io/safethread/docs)

## Contributing

We welcome contributions! If you'd like to contribute, please fork the repository and submit a pull request.

## Special thanks / Acknowledgments

- PyPi
- Python 3

## License and Copyright

Copyright (C) 2025 - Andre Luiz Romano Madureira

This project is licensed under the Apache License 2.0.  

For more details, see the full license text (see [``LICENSE``](./LICENSE) file).
