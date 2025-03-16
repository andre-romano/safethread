
import time
from safethread.thread import SchedulerThread

# Define the callback function

i = 0


def my_callback(arg) -> bool:
    global i
    i += 1
    print(f"Callback executed with argument: {arg}")
    if i == 3:
        return False
    return True


# Create a scheduler instance with the following parameters:
# - timeout: 2 seconds between each callback execution
# - callback: the `my_callback` function
# - args: a list containing the argument for the callback
# - repeat: True (repeat the callback indefinitely)
scheduler = SchedulerThread(
    timeout=2.0,
    callback=my_callback,
    args=["Hello, World!"],
    repeat=True
)

# Start the scheduler in a separate thread
scheduler.start()

# Stop the scheduler and Wait for the scheduler thread to finish
scheduler.join()

print("Scheduler stopped.")
