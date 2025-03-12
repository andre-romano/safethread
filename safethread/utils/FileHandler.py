
import queue
import threading

from typing import Any, Callable, Self

from ..thread import ThreadBase


class FileHandler:
    """
    A thread-safe asynchronous file handler that allows reading and writing operations 
    using separate threads, to ensure non-blocking behavior.
    """

    def __init__(self,
                 filename: str,
                 binary_mode: bool = False,
                 encoding: str | None = 'utf-8',
                 on_read: Callable[
                     [Any | None, Exception | None], None
                 ] = lambda data, e: None,
                 on_write: Callable[
                     [Any | None, Exception | None], None
                 ] = lambda data, e: None,
                 ) -> None:
        """
        Initializes the AsyncFileHandler.

        :param filename: Name of the file to read and write.
        :type filename: str        
        :param binary_mode: True, if files must be read/write using binary mode (non-text), False otherwise. Defaults to False (text-mode).
        :type binary_mode: bool
        :param encoding: File encoding to use. If None, locale.getencoding() is called to get the current locale encoding. Defaults to 'utf-8'.
        :type encoding: str
        :param on_read: A callback function that is called when data is read from a file.
                                The function should accept two arguments: data read, the Exception.                                
                                In case of error, data will be None, and exception will be passed as the second argument. Otherwise, exception will be None.
        :type on_read: Callable[[Any | None, Exception | None], None]
        :param on_write: A callback function that is called when data is written to a file.
                                The function should accept two argumenst: data written, the Exception.                                
                                In case of error, data will be None, and exception will be passed as the second argument. Otherwise, exception will be None.
        :type on_write: Callable[[Any | None, Exception | None], None]
        """
        self.__filename = filename
        self.__file_lock = threading.RLock()

        self.__binary_mode = binary_mode
        self.__encoding = encoding

        self.__on_read = on_read
        self.__on_write = on_write

        # write queue
        self.__queue_write = queue.Queue()

        # raw binary mode cannot have encoding
        if self.__binary_mode:
            self.__encoding = None

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
                        self.__on_read(line, None)
        except Exception as e:
            self.__on_read(None, e)

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
                        self.__on_write(data, None)
        except queue.Empty:
            # file write terminated successfully
            pass
        except Exception as e:
            self.__on_write(None, e)
        finally:
            self.__queue_write.shutdown(immediate=True)

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
        self.__thread_read = self.__thread_read.copy()  # reset the thread

    def join_write(self):
        """
        Joins the write thread, waiting for file writing operation to finish.

        :raises RuntimeError: if an attempt is made to join the current thread (main thread), or the join() is called before start()
        """
        self.__thread_write.join()
        self.__thread_write = self.__thread_write.copy()  # reset the thread
