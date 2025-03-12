
import threading
import multiprocessing

from multiprocessing.managers import ListProxy

from safethread.utils import HybridRLock

# Create an instance of HybridRLock
lock = HybridRLock()


def thread_safe_function():
    with lock:
        # Critical section of the code
        print(
            f"Thread {threading.current_thread().name} has acquired the lock")
        # Perform thread-safe operations here
        print(
            f"Thread {threading.current_thread().name} is releasing the lock")


def process_task(lock: HybridRLock, results: ListProxy):
    with lock:
        results.append(1)


def run_multithreaded_example():
    print("---------------------------------")
    print("Testing multi-threaded behaviour")
    print("---------------------------------")

    # Create multiple threads to demonstrate the usage of HybridRLock
    threads = []
    for i in range(5):
        thread = threading.Thread(
            target=thread_safe_function, name=f"Thread-{i}")
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All threads have completed execution")
    print(" ")


def run_multiprocessing_example():
    print("---------------------------------")
    print("Testing multi-processing behaviour")
    print("---------------------------------")

    results = multiprocessing.Manager().list()

    processes = [multiprocessing.Process(
        target=process_task, args=(lock, results)) for _ in range(10)]
    for process in processes:
        process.start()
    for process in processes:
        process.join()

    print(f"Results: {list(results)}")
    print("All processes have completed execution")
    print(" ")


if __name__ == "__main__":
    run_multithreaded_example()
    run_multiprocessing_example()
