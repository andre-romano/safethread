
from safethread.thread.utils import PipelineStageThreaded
from safethread.thread.utils import Pipeline

# creating pipeline and its stages (sequentially executed)
pipeline = Pipeline([
    PipelineStageThreaded(lambda x: x*2),
    PipelineStageThreaded(lambda x: x+1),
    PipelineStageThreaded(lambda x: x**2),
])

# starting pipeline
pipeline.start()
if pipeline.has_started():
    print(f"Pipeline has started")

# defining input and output values
input_values = [1, 2, 3]
expected_output_values = [9, 25, 49]

# sending input values to pipeline
for input_value in input_values:
    pipeline.put(input_value)

# getting results
for expected_output_value in expected_output_values:
    result = pipeline.get()
    print(f"Final result: {result} - Expected output: {expected_output_value}")

# stopping pipeline
pipeline.stop()
pipeline.join()

# checking pipeline state
if not pipeline.is_alive():
    print(f"Pipeline IS NOT alive")

if pipeline.is_terminated():
    print(f"Pipeline terminated")
