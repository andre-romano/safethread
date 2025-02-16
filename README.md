# safethread

[![PyPI](https://img.shields.io/pypi/v/safethread)](https://pypi.org/project/safethread/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](https://github.com/andre-romano/safethread/blob/main/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/safethread)](https://pypi.org/project/safethread/)

``safethread`` is a Python package that provides utilities for managing thread-safe operations and synchronization mechanisms. It includes custom data structures designed to ensure thread safety when used in multi-threaded programming.

## Features

- **Thread-Safe Data Structures**: 
  - `SafeList`: A thread-safe implementation of a list.
  - `SafeDict`: A thread-safe implementation of a dictionary.
- **Thread Synchronization**: Built-in locking mechanisms to ensure safe operations in multithreaded environments.
- **Utility Methods**: Additional helpers and utilities for threading and synchronization.

## Installation

You can install ``safethread`` from PyPI:

```bash
pip install safethread
```

## Usage

Check [``tests``](./tests/) folder and the full documentation (link below).

## Documentation

The full documentation is available in [``https://andre-romano.github.io/safethread/docs``](https://andre-romano.github.io/safethread/docs)

## Run automated tests (unit tests)

Run the following:

```batch
call .\install_dependencies.bat
call .\run_tests.bat
```

## Publish new version (PyPy and Github)

Run the following:

```batch
call .\install_dependencies.bat
call .\commit_version.bat
```

## Special thanks / Acknowledgments

- PyPi
- Python 3

## License and Copyright

Copyright (C) 2025 - Andre Luiz Romano Madureira

This project is licensed under the Apache License 2.0.  

For more details, see the full license text (see [``LICENSE``](./LICENSE) file).
