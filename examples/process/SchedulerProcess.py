
import time
from safethread.process.SchedulerProcess import SchedulerProcess


def task() -> bool:
    print("Task is running")
    return True  # continue running scheduler process


def main():
    scheduler = SchedulerProcess(
        timeout=0.1,
        callback=task,
        repeat=False,
    )

    try:
        print("Task is starting ...")
        begin = time.perf_counter()
        scheduler.start()  # Start the scheduler process
        scheduler.join()
        end = time.perf_counter()
        print(f"Task terminated in {end-begin} seconds")
    except KeyboardInterrupt:
        scheduler.stop()  # Stop the scheduler process on interrupt


if __name__ == "__main__":
    main()
