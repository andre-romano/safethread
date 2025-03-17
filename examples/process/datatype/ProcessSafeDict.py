import multiprocessing
# Replace with the actual import path
from safethread.process.datatype import ProcessSafeDict


def worker(safe_dict: ProcessSafeDict, key: str, value: int):
    """
    Worker function that adds a key-value pair to the shared dictionary.
    """
    safe_dict[key] = value
    print(f"Worker {key}: Dict after update -> {dict(safe_dict)}")


def main():
    # Create a process-safe dictionary
    safe_dict = ProcessSafeDict({"a": 1, "b": 2})  # Initialize with some data
    print("Initial dict:", dict(safe_dict))

    # Single-process operations
    safe_dict["c"] = 3
    print("After adding 'c':", dict(safe_dict))

    safe_dict.update({"d": 4, "e": 5})
    print("After update:", dict(safe_dict))

    del safe_dict["b"]
    print("After deleting 'b':", dict(safe_dict))

    # Multiprocessing operations
    processes = []
    for i in range(1, 5):  # Add key-value pairs ("f": 6), ("g": 7), ("h": 8), ("i": 9)
        key = chr(ord("f") + i - 1)  # Generate keys "f", "g", "h", "i"
        value = i + 5
        process = multiprocessing.Process(
            target=worker, args=(safe_dict, key, value))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print("Final dict after multiprocessing:", dict(safe_dict))


if __name__ == "__main__":
    main()
