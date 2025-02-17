
from safethread.thread import Pipeline

# A simple callback function that doubles the input number


def multiply_by_two(input_data):
    return input_data * 2


# Start pipeline with the 'multiply_by_two' function as the callback
pipeline = Pipeline(multiply_by_two)
pipeline.start()

# Put some values into the pipeline for processing
pipeline.put(5)
pipeline.put(10)
pipeline.put(15)

# Get and print the results
print(f"Processed result 1: {pipeline.get()}")  # Output: 10 (5 * 2)
print(f"Processed result 2: {pipeline.get()}")  # Output: 20 (10 * 2)
print(f"Processed result 3: {pipeline.get()}")  # Output: 30 (15 * 2)

# Join the thread to ensure it finishes execution before the program ends
pipeline.stop()
pipeline.join()
