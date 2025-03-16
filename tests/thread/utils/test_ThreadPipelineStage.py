import unittest

from safethread.thread.utils import ThreadPipelineStage


class TestThreadPipelineStage(unittest.TestCase):
    """
    Unit tests for the Pipeline class.
    """

    def test_invalid_initialization(self):
        """
        Test that an exception is raised when pipeline stage is improperly initialized.
        """
        with self.assertRaises(TypeError) as context:
            ThreadPipelineStage(None)  # type: ignore
        with self.assertRaises(ValueError) as context:
            ThreadPipelineStage(lambda x: x + 3, n_threads=0)  # type: ignore

    def test_put_and_get(self):
        """
        Test that data can be put into the pipeline, processed, and retrieved correctly.
        """
        pipeline = ThreadPipelineStage(lambda x: x * 2)
        test_input = 5
        expected_output = 10  # Since the callback doubles the input value

        pipeline.put(test_input)
        self.assertFalse(pipeline.has_started())
        self.assertFalse(pipeline.is_alive())

        # Run the pipeline
        pipeline.start()

        # Get the processed data
        result = pipeline.get()

        self.assertTrue(pipeline.has_started())
        self.assertTrue(pipeline.is_alive())

        self.assertEqual(result, expected_output)

        # stop pipeline and join
        pipeline.stop()
        pipeline.join()

    def test_concurrent_processing(self):
        """
        Test that the pipeline can handle multiple items in a concurrent setup.
        """
        # start the pipeline
        pipeline = ThreadPipelineStage(lambda x: x + 1, n_threads=5)
        pipeline.start()

        # Test multiple inputs
        inputs = [1, 2, 3, 4, 5]
        expected_outputs = [2, 3, 4, 5, 6]

        for item in inputs:
            pipeline.put(item)

        #  check results
        for expected in expected_outputs:
            result = pipeline.get()
            self.assertEqual(result, expected)

        # stop pipeline
        pipeline.stop()
        pipeline.join()

        # check if pipeline indeed stopped
        self.assertTrue(pipeline.has_started())
        self.assertFalse(pipeline.is_alive())
        self.assertTrue(pipeline.is_terminated())

    def test_concurrent_processing_after_put(self):
        """
        Test that the pipeline can handle multiple items in a concurrent setup.
        """
        # start the pipeline
        pipeline = ThreadPipelineStage(lambda x: x + 1, n_threads=5)

        # Test multiple inputs
        inputs = [1, 2, 3, 4, 5]
        expected_outputs = [2, 3, 4, 5, 6]

        for item in inputs:
            pipeline.put(item)

        pipeline.start()

        #  check results
        for expected in expected_outputs:
            result = pipeline.get()
            self.assertEqual(result, expected)

        # stop pipeline
        pipeline.stop()
        pipeline.join()

        # check if pipeline indeed stopped
        self.assertTrue(pipeline.has_started())
        self.assertFalse(pipeline.is_alive())
        self.assertTrue(pipeline.is_terminated())

    def test_stop_join(self):
        def multiply_by_two(input_data):
            return input_data * 2

        # Start pipeline with the 'multiply_by_two' function as the callback
        pipeline = ThreadPipelineStage(multiply_by_two)
        pipeline.start()

        # Test multiple inputs
        inputs = [5, 10, 15]
        expected_outputs = [10, 20, 30]

        for item in inputs:
            pipeline.put(item)

        #  check results
        for expected in expected_outputs:
            result = pipeline.get()
            self.assertEqual(result, expected)

        # Stop the thread immediately (no processing will be done)
        pipeline.stop()

        with self.assertRaises(ThreadPipelineStage.StoppedException) as context:
            pipeline.put(20)

        # Join to ensure it finishes execution before the program ends
        pipeline.join()

        # check if it finished properly
        self.assertEqual(pipeline.is_alive(), False)
        self.assertEqual(pipeline.is_terminated(), True)

    def test_pipeline_stopped_exception(self):
        """Tests that putting/getting data from a stopped pipeline raises an exception."""
        pipeline = ThreadPipelineStage(lambda x: None)
        pipeline.start()
        pipeline.stop()
        with self.assertRaises(ThreadPipelineStage.StoppedException):
            pipeline.put(5)
        with self.assertRaises(ThreadPipelineStage.StoppedException):
            pipeline.get()

    def test_connect_output(self):
        # Create two pipeline instances
        pipe1 = ThreadPipelineStage(lambda x: x+1)
        pipe2 = ThreadPipelineStage(lambda x: x*2)

        # Connect pipe1's output to pipe2's input
        pipe1.connect_output(pipe2)

        # start pipeline stages
        pipe1.start()
        pipe2.start()

        # Test multiple inputs
        inputs = [5, 10, 15]
        expected_outputs = [12, 22, 32]

        for item in inputs:
            pipe1.put(item)

        #  check results
        for expected in expected_outputs:
            result = pipe2.get()
            self.assertEqual(result, expected)

        # stop pipes
        pipe1.stop()
        pipe2.stop()

        # join pipes
        pipe1.join()
        pipe2.join()


if __name__ == '__main__':
    unittest.main()
