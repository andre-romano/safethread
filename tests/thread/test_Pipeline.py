import unittest

from safethread.thread import Pipeline, ThreadBase


class TestPipeline(unittest.TestCase):
    """
    Unit tests for the Pipeline class.
    """

    def test_invalid_callback(self):
        """
        Test that an exception is raised if the callback is not callable.
        """
        with self.assertRaises(ThreadBase.CallableException) as context:
            Pipeline(None)  # type: ignore

    def test_put_and_get(self):
        """
        Test that data can be put into the pipeline, processed, and retrieved correctly.
        """
        pipeline = Pipeline(lambda x: x * 2)
        test_input = 5
        expected_output = 10  # Since the callback doubles the input value

        pipeline.put(test_input)
        self.assertEqual(pipeline.has_started(), False)

        # Run the pipeline
        pipeline.start()

        # Get the processed data
        result = pipeline.get()

        self.assertEqual(pipeline.has_started(), True)
        self.assertEqual(pipeline.is_alive(), True)

        self.assertEqual(result, expected_output)

        # stop pipeline and join
        pipeline.stop()
        pipeline.join()

    def test_concurrent_processing(self):
        """
        Test that the pipeline can handle multiple items in a concurrent setup.
        """
        # start the pipeline
        pipeline = Pipeline(lambda x: x + 1)
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

    def test_concurrent_processing_after_put(self):
        """
        Test that the pipeline can handle multiple items in a concurrent setup.
        """
        # start the pipeline
        pipeline = Pipeline(lambda x: x + 1)

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

    def test_stop_join(self):
        def multiply_by_two(input_data):
            return input_data * 2

        # Start pipeline with the 'multiply_by_two' function as the callback
        pipeline = Pipeline(multiply_by_two)
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

        with self.assertRaises(Pipeline.StoppedException) as context:
            pipeline.put(20)

        # Join to ensure it finishes execution before the program ends
        pipeline.join()

        # check if it finished properly
        self.assertEqual(pipeline.is_alive(), False)
        self.assertEqual(pipeline.is_terminated(), True)


if __name__ == '__main__':
    unittest.main()
