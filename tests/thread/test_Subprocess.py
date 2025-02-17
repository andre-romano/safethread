import unittest
import sys

# Adjust the import to your module structure
from safethread.thread import Subprocess


class TestSubprocess(unittest.TestCase):

    def test_successful_execution(self):
        """Test if a simple command executes successfully across platforms."""
        if sys.platform == "win32":
            command = ["cmd", "/c", "echo Hello, World!"]
        else:
            command = ["echo", "Hello, World!"]
        sp = Subprocess(command)
        sp.start()
        sp.join()

        self.assertEqual(sp.get_stderr().strip(), "")
        self.assertEqual(sp.get_stdout().strip(), "Hello, World!")
        self.assertEqual(sp.get_return_code(), 0)
        self.assertTrue(sp.is_terminated())

    def test_failing_command(self):
        """Test if an invalid command raises an exception, handling platform differences."""
        command = ["non_existing_command"]
        sp = Subprocess(command)
        sp.start()
        sp.join()

        self.assertTrue(sp.is_terminated())
        self.assertEqual(sp.get_stdout(), "")
        self.assertNotEqual(sp.get_stderr(), "")
        self.assertNotEqual(sp.get_return_code(), 0)

    def test_stderr_output(self):
        """Test if stderr is correctly captured."""
        command = ["python", "-c",
                   "import sys; sys.stderr.write('Error Message\\n')"]

        sp = Subprocess(command)
        sp.start()
        sp.join()

        self.assertTrue(sp.is_terminated())
        self.assertEqual(sp.get_return_code(), 0)
        self.assertEqual(sp.get_stderr().strip(), "Error Message")

    def test_long_running_command(self):
        """Test handling of long-running processes in a cross-platform way."""
        command = ["python", "-c", "import time; time.sleep(0.1)"]

        sp = Subprocess(command)
        sp.start()
        self.assertFalse(sp.is_terminated())  # Should still be running

        sp.join()
        self.assertTrue(sp.is_terminated())  # Should be terminated now
        self.assertEqual(sp.get_return_code(), 0)

    def test_thread_safety(self):
        """Test multiple Subprocess instances running in parallel."""
        if sys.platform == "win32":
            command = ["cmd", "/c", "echo {{string}}"]
        else:
            command = ["echo", "{{string}}"]

        commands = [
            map(lambda x: x.replace('{{string}}',
                'Process 1'), command.copy()),
            map(lambda x: x.replace('{{string}}',
                'Process 2'), command.copy()),
            map(lambda x: x.replace('{{string}}',
                'Process 3'), command.copy())
        ]

        processes = [Subprocess(cmd) for cmd in commands]
        for p in processes:
            p.start()

        for p in processes:
            p.join()
            self.assertTrue(p.is_terminated())
            self.assertEqual(p.get_return_code(), 0)

        expected_outputs = ["Process 1", "Process 2", "Process 3"]
        actual_outputs = [p.get_stdout().strip() for p in processes]
        self.assertEqual(expected_outputs, actual_outputs)


if __name__ == "__main__":
    unittest.main()
