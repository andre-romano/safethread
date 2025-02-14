# safethread

[![PyPI](https://img.shields.io/pypi/v/safethread)](https://pypi.org/project/safethread/)
[![License](https://img.shields.io/github/license/andre-romano/safethread)](https://github.com/andre-romano/safethread/blob/main/LICENSE)

Python utilities classes for safe deployment and management of Threads, synchronization and Python data structures.

Includes:
- Thread-safe wrapper classes for most Python data structures
- Unit test for each class provided

## Installing

The library is available in ``pip`. You can install it using the command:
```batch
pip install safethread
```

## Usage

Check [``examples``](./examples/) and [``tests``](./tests/) folders.

## Documentation

Check [``docs``](./docs/) folder.

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

- Python 3

## License and Copyright

Copyright (C) 2025 - Andre Luiz Romano Madureira

This project is licensed under the Apache License 2.0.  

For more details, see the full license text (see [``LICENSE``](./LICENSE) file).
