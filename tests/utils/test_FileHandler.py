import os
import unittest

from safethread.utils import FileHandler


class TestAsyncFileHandler(unittest.TestCase):
    TEST_FILE = "test_async_file.txt"

    def setUp(self):
        """Creates a test file before each test."""
        with open(self.TEST_FILE, 'w', encoding='utf-8') as f:
            f.write("Line 1\nLine 2\nLine 3\n")

    def tearDown(self):
        """Removes the test file after each test."""
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

    def test_read_functionality(self):
        """Tests if asynchronous file reading works correctly."""
        handler = FileHandler(self.TEST_FILE)
        handler.start_read()

        lines = []
        while (line := handler.get()) is not None:
            lines.append(line.strip())

        self.assertEqual(lines, ["Line 1", "Line 2", "Line 3"])

        handler.join_read()

        status, error = handler.get_status()
        self.assertEqual(status, 0)
        self.assertEqual(error, "")

    def test_write_functionality(self):
        """Tests if asynchronous writing works correctly."""
        handler = FileHandler(self.TEST_FILE)
        handler.put("New Line 1\n")
        handler.put("New Line 2\n")
        handler.start_write()
        handler.join_write()

        status, error = handler.get_status()
        self.assertEqual(status, 0)
        self.assertEqual(error, "")

        with open(self.TEST_FILE, 'r', encoding='utf-8') as f:
            content = f.readlines()

        self.assertEqual(content, ["New Line 1\n", "New Line 2\n"])

    def test_write_after_shutdown(self):
        """Tests if attempting to write after thread termination raises an error."""
        handler = FileHandler(self.TEST_FILE)
        handler.start_write()
        handler.join_write()

        with self.assertRaises(RuntimeError):
            handler.put("Should Fail\n")

    def test_read_after_shutdown(self):
        """Tests if attempting to read after thread termination still returns data (as expected)."""
        handler = FileHandler(self.TEST_FILE)
        handler.start_read()
        handler.join_read()

        self.assertIsNotNone(handler.get())

    def test_join_before_start(self):
        # Test that joining a thread before starting it raises an error
        file_handler = FileHandler(self.TEST_FILE)

        with self.assertRaises(RuntimeError):
            file_handler.join_read()

        with self.assertRaises(RuntimeError):
            file_handler.join_write()

    def test_get_status(self):
        """Tests if status is returned correctly."""
        handler = FileHandler(self.TEST_FILE)
        status, error = handler.get_status()
        self.assertEqual(status, 0)
        self.assertEqual(error, "")

    def test_binary_file(self):
        file_handler = FileHandler(self.TEST_FILE, binary_mode=True)

        # Put data into buffer
        file_handler.put(b"Binary data\n")
        file_handler.put(b"More binary data\n")

        # Write data to the file
        file_handler.start_write()
        file_handler.join_write()

        # Read data from the file
        file_handler.start_read()
        file_handler.join_read()

        # Verify the read data
        self.assertEqual(file_handler.get(), b"Binary data\n")
        self.assertEqual(file_handler.get(), b"More binary data\n")
        self.assertIsNone(file_handler.get())  # Queue should be empty

    def test_error_handling(self):
        # Test error handling during file operations
        file_handler = FileHandler("non_existent_file.txt")

        # Attempt to read from a non-existent file
        file_handler.start_read()
        file_handler.join_read()

        # Check for error status
        status, error = file_handler.get_status()
        self.assertEqual(status, 1)
        self.assertIn("No such file or directory", error)


if __name__ == "__main__":
    unittest.main()
