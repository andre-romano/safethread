import multiprocessing

from safethread.process.datatype import ProcessSafeList


def worker(safe_list: ProcessSafeList, value: int):
    """
    Worker function that appends a value to the shared list.
    """
    safe_list.append(value)
    print(f"Worker {value}: List after append -> {list(safe_list)}")


def main():
    # Create a process-safe list
    safe_list = ProcessSafeList([1, 2, 3])  # Initialize with some data
    print("Initial list:", list(safe_list))

    # Single-process operations
    safe_list.append(4)
    print("After append:", list(safe_list))

    safe_list.extend([5, 6])
    print("After extend:", list(safe_list))

    safe_list.remove(2)
    print("After remove:", list(safe_list))

    safe_list.reverse()
    print("After reverse:", list(safe_list))

    safe_list.sort()
    print("After sort:", list(safe_list))

    # Multiprocessing operations
    processes = []
    for i in range(7, 11):  # Append values 7, 8, 9, 10
        process = multiprocessing.Process(target=worker, args=(safe_list, i))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print("Final list after multiprocessing:", list(safe_list))


if __name__ == "__main__":
    main()
