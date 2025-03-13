
import time
from safethread.thread import SchedulerThread

# Define the callback function


def my_callback(arg):
    print(f"Callback executed with argument: {arg}")


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

# Let the scheduler run for a while (e.g., 3 executions - 6 seconds)
time.sleep(5.0)

# Stop the scheduler and Wait for the scheduler thread to finish
scheduler.stop()
scheduler.join()

print("Scheduler stopped.")
