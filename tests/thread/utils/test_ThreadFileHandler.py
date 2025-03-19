import logging
import os
import stat
import time
import unittest
import tracemalloc

from safethread.thread.utils import ThreadFileHandler


class TestThreadFileHandler(unittest.TestCase):
    @staticmethod
    def create_file(filename):
        try:
            with open(filename, 'x') as file:
                pass
        except:
            pass

    @staticmethod
    def remove_file(filename):
        while os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                time.sleep(0.05)

    @staticmethod
    def set_file_permissions(filename, permissions):
        while os.path.exists(filename):
            try:
                os.chmod(filename, permissions)
                break
            except:
                time.sleep(0.05)

    def setUp(self):
        """Creates a test file before each test."""
        # clear result obj
        self.__result_read = []
        self.__result_write = []

    def test_write_read(self):
        """Tests if asynchronous file write / reading works correctly."""
        def on_read(data, e):
            self.__result_read.append(data)
            if e:
                raise e

        def on_write(data, e):
            self.__result_write.append(data)
            if e:
                raise e

        test_filename = "test_file1.txt"
        TestThreadFileHandler.create_file(test_filename)

        handler = ThreadFileHandler(
            test_filename,
            on_read=on_read,
            on_write=on_write,
        )

        handler.put("Line 1\n")
        handler.put("Line 2\n")
        handler.put("Line 3\n")

        handler.start_write()
        handler.join_write()

        self.assertTrue(self.__result_write == [
                        "Line 1\n", "Line 2\n", "Line 3\n"])

        handler.start_read()
        handler.join_read()

        self.assertTrue(self.__result_read == [
                        "Line 1\n", "Line 2\n", "Line 3\n"])

        TestThreadFileHandler.remove_file(test_filename)

    def test_write_after_shutdown(self):
        """Tests if attempting to write after thread termination raises an error."""

        test_filename = "test_file3.txt"

        TestThreadFileHandler.create_file(test_filename)
        handler = ThreadFileHandler(test_filename)
        handler.start_write()
        handler.join_write()

        with self.assertRaises(RuntimeError):
            handler.put("Should Fail\n")

        TestThreadFileHandler.remove_file(test_filename)

    def test_join_before_start(self):
        # Test that joining a thread before starting it raises an error

        test_filename = "test_file4.txt"
        TestThreadFileHandler.create_file(test_filename)
        file_handler = ThreadFileHandler(test_filename)

        with self.assertRaises(RuntimeError):
            file_handler.join_read()

        with self.assertRaises(RuntimeError):
            file_handler.join_write()

        TestThreadFileHandler.remove_file(test_filename)

    def test_binary_file(self):
        def on_read(data, e):
            self.__result_read.append(data)
            if e:
                raise e

        def on_write(data, e):
            self.__result_write.append(data)
            if e:
                raise e

        test_filename = "test_file5.txt"
        TestThreadFileHandler.create_file(test_filename)

        file_handler = ThreadFileHandler(
            test_filename,
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
        self.assertTrue(self.__result_read == [
            b"Binary data\n",
            b"More binary data\n",
        ])

        TestThreadFileHandler.remove_file(test_filename)

    def test_read_error(self):
        def on_read(data, e):
            self.assertIsNone(data)
            self.assertIsNotNone(e)
            self.assertIsInstance(e, Exception)

        # Create a FileHandler instance with the mock callback
        file_handler = ThreadFileHandler(
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

        test_filename = "test_file6.txt"
        TestThreadFileHandler.create_file(test_filename)

        # Create a FileHandler instance with the mock callback
        file_handler = ThreadFileHandler(
            filename=test_filename,
            on_write=on_write,
        )

        # Set the file permissions to read-only
        self.set_file_permissions(
            test_filename, stat.S_IRUSR)

        # Add data to the write queue
        file_handler.put("Test data")

        # Start the write thread
        file_handler.start_write()
        file_handler.join_write()

        # Reset file permissions
        self.set_file_permissions(
            test_filename, stat.S_IRUSR | stat.S_IWUSR)

        TestThreadFileHandler.remove_file(test_filename)


if __name__ == "__main__":
    tracemalloc.start()
    unittest.main()
