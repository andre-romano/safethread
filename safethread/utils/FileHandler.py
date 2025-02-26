
import queue
import threading

from typing import Any, Iterable, Self

from ..thread import ThreadBase


class FileHandler:
    """
    A thread-safe asynchronous file handler that allows reading and writing operations 
    using separate threads and queues to ensure non-blocking behavior.
    """

    def __init__(self, filename: str, max_queue_read_size: int = 100, binary_mode: bool = False, encoding: str | None = 'utf-8') -> None:
        """
        Initializes the AsyncFileHandler.

        :param filename: Name of the file to read and write.
        :type filename: str
        :param max_queue_read_size: Maximum number of lines stored in the read queue. Defaults to 100.
        :type max_queue_read_size: int
        :param binary_mode: True, if files must be read/write using binary mode (non-text), False otherwise. Defaults to False (text-mode).
        :type binary_mode: bool
        :param encoding: File encoding to use. If None, locale.getencoding() is called to get the current locale encoding. Defaults to 'utf-8'.
        :type encoding: str
        """
        self.__filename = filename
        self.__file_lock = threading.RLock()
        self.__binary_mode = binary_mode
        self.__encoding = encoding

        # raw binary mode cannot have encoding
        if self.__binary_mode:
            self.__encoding = None

        # queues
        self.__queue_read = queue.Queue(maxsize=max_queue_read_size)
        self.__queue_write = queue.Queue()

        # error string
        self.__error = ""

        # create threads
        self.__thread_read = ThreadBase(self.__read)
        self.__thread_write = ThreadBase(self.__write)

    def __read(self):
        """
        Reads lines from the file and adds them to the read queue.
        """
        try:
            mode = 'r' + ('b' if self.__binary_mode else '')
            with self.__file_lock:
                with open(self.__filename, mode=mode, encoding=self.__encoding) as f:
                    for line in f:
                        self.__queue_read.put(line)
        except Exception as e:
            self.__error = str(e)
        finally:
            self.__queue_read.shutdown()

    def __write(self):
        """
        Writes data from the write queue into the file.
        """
        try:
            mode = 'w' + ('b' if self.__binary_mode else '')
            with self.__file_lock:
                with open(self.__filename, mode=mode, encoding=self.__encoding) as f:
                    while True:
                        data = self.__queue_write.get_nowait()
                        f.write(data)
        except queue.Empty:
            # file write terminated successfully
            pass
        except Exception as e:
            self.__error = str(e)
        finally:
            self.__queue_write.shutdown(immediate=True)

    def get(self) -> Any | None:
        """
        Retrieves a line from the read queue (buffer).

        :return: A line from the file, or None if the queue is empty.
        """
        try:
            return self.__queue_read.get()
        except (queue.Empty, queue.ShutDown):
            return None

    def put(self, data) -> Self:
        """
        Adds a data to the write queue (buffer).

        :param data: The data to be written to the file.

        :return: This file handler object.

        :raises RuntimeError: if the write thread has terminated.
        """
        try:
            self.__queue_write.put(data)
        except queue.ShutDown:
            raise RuntimeError(
                "Cannot put data to write to file after async write() terminated")
        return self

    def get_status(self):
        """
        Retrieves the current status of async read() / write() operations.

        :return: A tuple containing a status code (0 for success, 1 for error) and an error message if any.
        """
        status = 0 if not self.__error else 1
        return (status, self.__error)

    def start_read(self):
        """
        Starts the file reader thread.

        :raises RuntimeError: if start_read() is called more than once.
        """
        self.__thread_read.start()

    def start_write(self):
        """
        Starts the file writer thread.

        :raises RuntimeError: if start_write() is called more than once.
        """
        self.__thread_write.start()

    def join_read(self):
        """
        Joins the read thread, waiting for file reading operation to finish.

        :raises RuntimeError: if an attempt is made to join the current thread (main thread), or the join() is called before start()
        """
        self.__thread_read.join()

    def join_write(self):
        """
        Joins the write thread, waiting for file writing operation to finish.

        :raises RuntimeError: if an attempt is made to join the current thread (main thread), or the join() is called before start()
        """
        self.__thread_write.join()
