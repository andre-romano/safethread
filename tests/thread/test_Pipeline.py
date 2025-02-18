import queue
import unittest

from queue import Queue

from safethread.thread import Pipeline


class TestPipeline(unittest.TestCase):
    """
    Unit tests for the Pipeline class.
    """

    def setUp(self):
        """
        This method is called before each test case.
        """
        # A simple callback function for testing
        def callback(input_data):
            return input_data * 2

        self.pipeline = Pipeline(callback)

    def tearDown(self) -> None:
        if self.pipeline.has_started() and self.pipeline.is_alive():
            self.pipeline.stop()
            self.pipeline.join()

    def test_pipeline_initialization(self):
        """
        Test that the pipeline is initialized correctly.
        """
        self.assertIsInstance(self.pipeline, Pipeline)
        self.assertIsInstance(self.pipeline._input_queue, Queue)
        self.assertIsInstance(self.pipeline._output_queue, Queue)

    def test_invalid_callback(self):
        """
        Test that an exception is raised if the callback is not callable.
        """
        with self.assertRaises(Exception) as context:
            Pipeline(None)  # type: ignore

    def test_put_and_get(self):
        """
        Test that data can be put into the pipeline, processed, and retrieved correctly.
        """
        test_input = 5
        expected_output = 10  # Since the callback doubles the input value

        self.pipeline.put(test_input)
        self.assertEqual(self.pipeline.has_started(), False)

        # Run the pipeline
        self.pipeline.start()

        self.assertEqual(self.pipeline.has_started(), True)
        self.assertEqual(self.pipeline.is_alive(), True)

        # Get the processed data
        result = self.pipeline.get()

        self.assertEqual(result, expected_output)

    def test_concurrent_processing(self):
        """
        Test that the pipeline can handle multiple items in a concurrent setup.
        """
        # start the pipeline
        self.pipeline = Pipeline(lambda x: x + 1)
        self.pipeline.start()

        # Test multiple inputs
        inputs = [1, 2, 3, 4, 5]
        expected_outputs = [2, 3, 4, 5, 6]

        for item in inputs:
            self.pipeline.put(item)

        #  check results
        for expected in expected_outputs:
            result = self.pipeline.get()
            self.assertEqual(result, expected)

    def test_concurrent_processing_after_put(self):
        """
        Test that the pipeline can handle multiple items in a concurrent setup.
        """
        # start the pipeline
        self.pipeline = Pipeline(lambda x: x + 1)

        # Test multiple inputs
        inputs = [1, 2, 3, 4, 5]
        expected_outputs = [2, 3, 4, 5, 6]

        for item in inputs:
            self.pipeline.put(item)

        self.pipeline.start()

        #  check results
        for expected in expected_outputs:
            result = self.pipeline.get()
            self.assertEqual(result, expected)

    def test_stop_join(self):
        def multiply_by_two(input_data):
            return input_data * 2

        # Start pipeline with the 'multiply_by_two' function as the callback
        self.pipeline = Pipeline(multiply_by_two)
        self.pipeline.start()

        # Put some values into the self.pipeline for processing
        self.pipeline.put(5)
        self.pipeline.put(10)
        self.pipeline.put(15)

        # Expected outputs
        expected_outputs = [10, 20, 30]

        # Join the thread to ensure it finishes execution before the program ends
        self.pipeline.stop()

        with self.assertRaises(Pipeline.StoppedException) as context:
            self.pipeline.put(20)

        self.pipeline.join()

        #  check results
        for expected in expected_outputs:
            result = self.pipeline.get()
            self.assertEqual(result, expected)

        self.assertEqual(self.pipeline.is_alive(), False)
        self.assertEqual(self.pipeline.is_terminated(), True)


if __name__ == '__main__':
    unittest.main()
