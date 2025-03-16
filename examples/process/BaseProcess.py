from multiprocessing import Value
from multiprocessing.sharedctypes import Synchronized
import time

from safethread.process.BaseProcess import BaseProcess

# init a process-safe integer
# (result.value = 0)
result = Value("f", 0.0)


def run(process_name: str, result: Synchronized, *args) -> bool:
    # calculate sum of args
    s = 0.0
    for arg in args:
        s += arg

    print(f"----------------------")
    print(f"  Process is running   ")
    print(f"                      ")
    print(f"  run({process_name}, ...) ")
    print(f"----------------------")
    print(f"Local Sum: {s}")
    print(f" ")

    # store result in process-shared integer value
    with result.get_lock():
        result.value += s

    return False  # stop process here


def on_end(e: Exception | None):
    if e:
        print(f"ERROR: {e}")
        raise e
    print(f"Process executed successfully")


if __name__ == "__main__":
    # number of threads to create
    n_processs: int = 5

    # input data
    input_data = [i for i in range(int(30e6))]
    input_len = len(input_data)
    chunk_size = int(input_len/n_processs)

    # create processs
    processs: list[BaseProcess] = []
    for i in range(n_processs):
        # get input for given process
        begin = i*chunk_size
        end = min(begin+chunk_size, input_len)
        process_input = input_data[begin:end]

        processs.append(
            BaseProcess(
                callback=run,
                args=[f"Process {i}", result] + process_input,
                on_end=on_end,
            )
        )

    # expected result
    begin = time.perf_counter()
    expected_result = 0.0
    for arg in input_data:
        expected_result += arg
    expected_time = (time.perf_counter() - begin)*1000

    # starting processs
    begin = time.perf_counter()
    for t in processs:
        t.start()

    # waiting for them to finish
    for t in processs:
        t.join()
    processes_time = (time.perf_counter() - begin)*1000
    print(f" ")
    print(f"All processes terminated")
    print(f" ")

    # get shared variable result
    with result.get_lock():
        print(f"----------------------")
        print(f"  Result: {result.value} - Expected result: {expected_result}")
        print(f"  ({processes_time} msec) - ({expected_time} msec)")
        print(f"----------------------")
