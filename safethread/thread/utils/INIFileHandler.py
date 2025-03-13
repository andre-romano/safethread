import os
import configparser
import threading

from typing import Callable, Self

from .. import BaseThread


class INIFileHandler:
    """
    A thread-safe class to handle async reading and writing configuration files in INI format.    
    """

    def __init__(self,
                 filename: str,
                 create_default: bool = False,
                 on_read: Callable[
                     [Self, Exception | None], None
                 ] = lambda ini, e: None,
                 on_write: Callable[
                     [Self, Exception | None], None
                 ] = lambda ini, e: None,
                 ):
        """
        Initialize the ConfigParser object.
        :param filename: The name of the configuration file.
        :type filename: str
        :param create_default: Flag to create default configuration if the file does not exist, defaults to False.
        :type create_default: bool, optional
        :param on_read: Callback function to be called after reading the configuration file. It receives this INI object and an Exception or None.
        :type on_read: Callable[[Self, Exception | None], None], optional
        :param on_write: Callback function to be called after writing to the configuration file. It receives this INI object and an Exception or None.
        :type on_write: Callable[[Self, Exception | None], None], optional
        """
        # file lock
        self.__filename = filename
        self.__file_lock = threading.RLock()

        # on read and write callbacks
        self.__on_read = on_read
        self.__on_write = on_write

        # create threads
        self.__thread_read = BaseThread(self.__read)
        self.__thread_write = BaseThread(self.__write)

        # configuration parser
        self._config = configparser.ConfigParser()

        if create_default:
            self._init_default_data()

    def __read(self):
        """
        Loads the configurations from the INI file 
        """
        try:
            with self.__file_lock:
                if (not self.__filename) or (not os.path.exists(self.__filename)):
                    raise FileNotFoundError(
                        f"File '{self.__filename}' not found")
                n_files = self._config.read(self.__filename, encoding='utf-8')
            if not n_files:
                raise OSError(f"File '{self.__filename}' cannot be read.")
            self.__on_read(self, None)
        except Exception as e:
            self.__on_read(self, e)

    def __write(self):
        """
        Saves the configurations to the INI file.
        """
        try:
            with self.__file_lock:
                with open(self.__filename, 'w', encoding='utf-8') as configfile:
                    self._config.write(configfile)
            self.__on_write(self, None)
        except Exception as e:
            self.__on_write(self, e)

    def __getitem__(self, sec_option: str):
        return self.get(sec_option)

    def __setitem__(self, sec_option: str, value):
        return self.set(sec_option, value)

    def _init_default_data(self):
        """
        Initialize default data for the ConfigParser.

        This method should be overloaded in subclasses to provide specific
        default data initialization. If not overloaded, it raises a RuntimeError.

        :raises RuntimeError: If the method is not overloaded in a subclass.
        """

        raise RuntimeError(f"ConfigParser._init_default_data() NOT overloaded")

    def get(self, sec_option: str, fallback: str = ''):
        """
        Gets a configuration value with a fallback option.
        Format: 'section.option' 

        :param sec_option: Section and option to get the value from.
        :type sec_option: str
        :param fallback: Fallback value to return if the section or option is not found.
        :type fallback: str
        """
        section, option = sec_option.split('.')
        return str(self._config.get(section, option, fallback=fallback)).strip()

    def set(self, sec_option: str, value: str):
        """
        Sets a value in the configuration.
        Format: 'section.option' 

        :param sec_option: Section and option to set the value for.
        :type sec_option: str
        :param value: Value to be set. 
        :type value: str
        """
        section, option = sec_option.split('.')
        if not self._config.has_section(section):
            self._config.add_section(section)
        self._config.set(section, option, value)

    def show_all(self):
        """
        Shows all loaded configurations.
        """
        for section in self._config.sections():
            print(f"[{section}]")
            for key, value in self._config.items(section):
                print(f"{key} = {value}")
            print()

    def start_read(self):
        """
        Starts the file reader thread.

        :raises RuntimeError: if read thread is already running.
        """
        self.__thread_read.start()

    def start_write(self):
        """
        Starts the file writer thread.

        :raises RuntimeError: if write thread is already running.
        """
        self.__thread_write.start()

    def join_read(self):
        """
        Joins the read thread, waiting read operation to finish.

        :raises RuntimeError: if an attempt is made to join the current thread (main thread), or the join() is called before start()
        """
        self.__thread_read.join()
        self.__thread_read = self.__thread_read.copy()  # reset the thread

    def join_write(self):
        """
        Joins the write thread, waiting write operation to finish.

        :raises RuntimeError: if an attempt is made to join the current thread (main thread), or the join() is called before start()
        """
        self.__thread_write.join()
        self.__thread_write = self.__thread_write.copy()  # reset the thread
