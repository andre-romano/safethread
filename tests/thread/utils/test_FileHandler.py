import os
import stat
import unittest

from safethread.thread.utils import FileHandler


class TestAsyncFileHandler(unittest.TestCase):
    TEST_FILE = "test_async_file.txt"

    def setUp(self):
        """Creates a test file before each test."""
        # clear result obj
        self.__result = []

        # guarantee that the file is writeable
        if os.path.exists(self.TEST_FILE):
            os.chmod(self.TEST_FILE, stat.S_IRUSR | stat.S_IWUSR)

        # Create a test file with some content
        with open(self.TEST_FILE, 'w', encoding='utf-8') as f:
            f.write("Line 1\nLine 2\nLine 3\n")

    def tearDown(self):
        """Removes the test file after each test."""
        if os.path.exists(self.TEST_FILE):
            # Restore write permissions
            os.chmod(self.TEST_FILE, stat.S_IRUSR | stat.S_IWUSR)
            os.remove(self.TEST_FILE)

    def test_read_functionality(self):
        """Tests if asynchronous file reading works correctly."""
        def on_read(data, e):
            self.__result.append(data)
            if e:
                raise e

        handler = FileHandler(
            self.TEST_FILE,
            on_read=on_read
        )
        handler.start_read()

        handler.join_read()
        self.assertEqual(self.__result, ["Line 1\n", "Line 2\n", "Line 3\n"])

    def test_write_functionality(self):
        """Tests if asynchronous writing works correctly."""
        def on_write(data, e):
            self.__result.append(data)
            if e:
                raise e

        handler = FileHandler(
            self.TEST_FILE,
            on_write=on_write
        )

        # Put data into buffer
        handler.put("New Line 1\n")
        handler.put("New Line 2\n")

        # Write data to the file
        handler.start_write()
        handler.join_write()

        content = []
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

    def test_join_before_start(self):
        # Test that joining a thread before starting it raises an error
        file_handler = FileHandler(self.TEST_FILE)

        with self.assertRaises(RuntimeError):
            file_handler.join_read()

        with self.assertRaises(RuntimeError):
            file_handler.join_write()

    def test_binary_file(self):
        def on_read(data, e):
            self.__result.append(data)
            if e:
                raise e

        def on_write(data, e):
            if e:
                raise e

        file_handler = FileHandler(
            self.TEST_FILE,
            binary_mode=True,
            on_read=on_read,
            on_write=on_write,
        )

        # Put data into buffer
        file_handler.put(b"Binary data\n")
        file_handler.put(b"More binary data\n")

        # Write data to the file
        file_handler.start_write()
        file_handler.join_write()

        # Read data from the file
        file_handler.start_read()
        file_handler.join_read()

        # Verify the content of the file
        self.assertEqual(self.__result, [
            b"Binary data\n",
            b"More binary data\n",
        ])

    def test_read_error(self):
        def on_read(data, e):
            self.assertIsNone(data)
            self.assertIsNotNone(e)
            self.assertIsInstance(e, Exception)

        # Create a FileHandler instance with the mock callback
        file_handler = FileHandler(
            filename="non_existent_file.txt",  # Use a non-existent file to trigger an error
            on_read=on_read,
        )

        # Attempt to read from a non-existent file
        file_handler.start_read()
        file_handler.join_read()

    def test_write_error(self):
        """
        Test that the `on_write_error` callback is called when an error occurs during writing.
        """
        def on_write(data, e):
            self.assertIsNone(data)
            self.assertIsNotNone(e)
            self.assertIsInstance(e, Exception)

        # Create a FileHandler instance with the mock callback
        file_handler = FileHandler(
            filename=self.TEST_FILE,
            on_write=on_write,
        )

        # Set the file permissions to read-only
        os.chmod(self.TEST_FILE, stat.S_IRUSR)  # Read-only for the owner

        # Add data to the write queue
        file_handler.put("Test data")

        # Start the write thread
        file_handler.start_write()
        file_handler.join_write()


if __name__ == "__main__":
    unittest.main()
