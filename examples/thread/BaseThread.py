
import time
from safethread.thread.BaseThread import BaseThread

from safethread.thread.datatype import ThreadRLock

result = 0.0
lock = ThreadRLock()


def run(thread_name: str, *args) -> bool:
    global result, lock

    # calculate sum of args
    s = 0.0
    for arg in args:
        s += arg

    print(f"----------------------")
    print(f"  Thread is running   ")
    print(f"                      ")
    print(f"  run({thread_name},  ...) ")
    print(f"----------------------")
    print(f"Local Sum: {s}")
    print(f" ")

    # store result into shared variable
    with lock:
        result += s

    return False  # stop Thread here


def on_end(e: Exception | None):
    if e:
        print(f"ERROR: {e}")
        raise e
    print(f"Thread executed successfully")


if __name__ == "__main__":
    # number of threads to create
    n_threads: int = 5

    # input data
    input_data = [i for i in range(int(30e6))]
    input_len = len(input_data)
    chunk_size = int(input_len/n_threads)

    # create threads
    threads: list[BaseThread] = []
    for i in range(n_threads):
        # get input for given thread
        begin = i*chunk_size
        end = min(begin+chunk_size, input_len)
        thread_input = input_data[begin:end]

        threads.append(
            BaseThread(
                callback=run,
                args=[f"Thread {i}"] + thread_input,
                on_end=on_end,
            )
        )

    # expected result
    begin = time.perf_counter()
    expected_result = 0.0
    for arg in input_data:
        expected_result += arg
    expected_time = (time.perf_counter() - begin)*1000

    # starting threads
    begin = time.perf_counter()
    for t in threads:
        t.start()

    # waiting for them to finish
    for t in threads:
        t.join()
    threads_time = (time.perf_counter() - begin)*1000
    print(f" ")
    print("All threads terminated  ")
    print(f" ")

    # get shared variable result
    with lock:
        print(f"----------------------")
        print(f"  Result: {result} - Excepted result: {expected_result}")
        print(f"  ({threads_time} msec) - ({expected_time} msec)")
        print(f"----------------------")
