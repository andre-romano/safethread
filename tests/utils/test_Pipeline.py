import unittest

from safethread.utils import PipelineStage, Pipeline

# Assuming the `Pipeline` and `PipelineStage` classes are already imported
# from your module, the mock `PipelineStage` is needed to test the `Pipeline`.


class TestPipeline(unittest.TestCase):

    def test_single_stage(self):
        """Test that single stage pipeline."""
        pipeline = Pipeline([
            PipelineStage(lambda x: x+5),
        ])

        # Test multiple inputs
        inputs = [5, 10, 15]
        expected_outputs = [10, 15, 20]

        self.assertFalse(pipeline.has_started())
        self.assertFalse(pipeline.is_terminated())

        # start pipeline stages
        pipeline.start()

        self.assertTrue(pipeline.has_started())
        self.assertTrue(pipeline.is_alive())
        self.assertFalse(pipeline.is_terminated())

        for item in inputs:
            pipeline.put(item)

        #  check results
        for expected in expected_outputs:
            result = pipeline.get()
            self.assertEqual(result, expected)

        # stop and join pipeline
        pipeline.stop()
        pipeline.join()

        self.assertTrue(pipeline.has_started())
        self.assertFalse(pipeline.is_alive())
        self.assertTrue(pipeline.is_terminated())

    def test_multi_stage(self):
        """Test that multi stage pipeline."""
        pipeline = Pipeline([
            PipelineStage(lambda x: x+5),
            PipelineStage(lambda x: x**2),
        ])

        # Test multiple inputs
        inputs = [-10, -15, -20]
        expected_outputs = [25, 100, 225]

        self.assertFalse(pipeline.has_started())
        self.assertFalse(pipeline.is_terminated())

        # start pipeline stages
        pipeline.start()

        self.assertTrue(pipeline.has_started())
        self.assertTrue(pipeline.is_alive())
        self.assertFalse(pipeline.is_terminated())

        for item in inputs:
            pipeline.put(item)

        #  check results
        for expected in expected_outputs:
            result = pipeline.get()
            self.assertEqual(result, expected)

        # stop and join pipeline
        pipeline.stop()
        pipeline.join()

        self.assertTrue(pipeline.has_started())
        self.assertFalse(pipeline.is_alive())
        self.assertTrue(pipeline.is_terminated())


if __name__ == "__main__":
    unittest.main()
