import logging
import os
import threading

from logging import FileHandler, Formatter, StreamHandler
from venv import logger

from .Singleton import Singleton


class Log(Singleton):

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR

    __loggers = set()
    __loggers_lock = threading.RLock()

    __handlers: list[logging.Handler] = []

    def __init__(
        self,
        logfile: str = "",
        log_level: int = DEBUG,
        log_format: str = "%(asctime)s - [%(levelname)s] - %(name)s.%(funcName)s(): %(message)s",
        date_format: str = "%Y-%m-%d %H:%M:%S",
    ):
        """
        Initializes and configures the thread-safe logging system.

        :param logfile: Path to the log file. If not provided, logs will only be printed to the console.
        :type logfile: str, optional
        :param log_level: The minimum log level to display. Defaults to INFO.
        :type log_level: int, optional
        :param log_format: The format of the log messages. Defaults to a '%(asctime)s - [%(levelname)s] - %(name)s.%(funcName)s(): %(message)s'.
        :type log_format: str, optional
        :param date_format: The format of the date and time in log messages. Defaults to ' %Y-%m-%d %H:%M:%S '.
        :type date_format: str, optional
        """
        # configure logging
        self.__logfile = logfile
        self.__log_level = log_level
        self.__log_format = log_format
        self.__date_format = date_format

        # Create formatter
        formatter = Formatter(self.__log_format, self.__date_format)

        # Console handler
        console_handler = StreamHandler()
        console_handler.setFormatter(formatter)
        self.__handlers.append(console_handler)

        # File handler (if a log file is provided)
        if self.__logfile:
            file_handler = FileHandler(
                self.__logfile,
                mode="a",
                encoding="utf-8"
            )
            file_handler.setFormatter(formatter)
            self.__handlers.append(file_handler)

    def __del__(self):
        """Destructor for the Log class."""
        # ensures all logs are written to disk, and all handlers are closed
        self.shutdown()

    def __getitem__(self, name: str) -> logging.Logger:
        """
        Retrieves a logger with the specified name.

        :param name: The name of the logger.
        :type name: str
        """
        return self.get_logger(name)

    def __create_logger(self, name: str) -> logging.Logger:
        """
        Creates a logger with the specified name.

        :param name: The name of the logger.
        :type name: str
        """
        # Create a logger
        logger = logging.getLogger(name)
        logger.setLevel(self.__log_level)
        logger.handlers.clear()  # Prevent duplicate handlers
        for handler in self.__handlers:
            logger.addHandler(handler)  # Add handlers to the logger
        # add handler to set of loggers
        self.__loggers.add(name)
        return logger

    def get_logfile(self) -> str:
        """
        Retrieves the path to the log file.

        :return: The path to the log file.
        :rtype: str
        """
        return self.__logfile

    def get_level(self) -> int:
        """
        Retrieves the minimum log level to display.

        :return: The minimum log level to display.
        :rtype: int
        """
        return self.__log_level

    def get_log_format(self) -> str:
        """
        Retrieves the format of the log messages.

        :return: The format of the log messages.
        :rtype: str
        """
        return self.__log_format

    def get_date_format(self) -> str:
        """
        Retrieves the format of the date and time in log messages.

        :return: The format of the date and time in log messages.
        :rtype: str
        """
        return self.__date_format

    def get_logger(self, name: str) -> logging.Logger:
        """
        Retrieves a logger with the specified name.

        :param name: The name of the logger.
        :type name: str

        :return: The logger with the specified name.
        :rtype: logging.Logger        
        """
        with self.__loggers_lock:
            if name not in self.__loggers:
                return self.__create_logger(name)
            return logging.getLogger(name)

    def flush_logs_from(self, name: str):
        """
        Flushes logs from logger with the specified name.

        :param name: The name of the logger.
        :type name: str
        """
        logger = self.get_logger(name)
        for handler in logger.handlers:
            handler.flush()

    @staticmethod
    def flush_all_logs():
        """Flushes all log handlers to ensure logs are written to disk."""
        for logger_name in logging.root.manager.loggerDict:
            _logger = logging.getLogger(logger_name)
            for handler in _logger.handlers:
                try:
                    handler.flush()
                except:
                    pass

    def shutdown(self):
        """
        Shutdowns the logging system.

        Perform any necessary cleanup actions (e.g. flushing buffers).

        Should be called at application exit.
        """
        # Flush all logs to ensure they are written to disk
        try:
            logging.shutdown()
        except:
            pass
