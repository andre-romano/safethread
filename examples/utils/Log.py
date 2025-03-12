
import os

from safethread.utils import Log

# store logs into a file
logfile = "example.log"

# Create an instance of the Log class
log = Log.get_instance(
    logfile=logfile,
    log_level=Log.DEBUG
)

# Log some messages


def first_function():
    logger = log.get_logger(__name__)

    logger.info("This is an info message.")
    logger.debug("This is a debug message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")


def second_function():
    logger2 = log.get_logger("second_logger")

    logger2.critical("Critical message from other logger.")


def remove_logfile():
    # should be called before removing the logfile
    log.shutdown()  # it is a good practice
    # if not explicitly called at the end of your program,
    # the Python __del__() destructor will call it

    # remove logfile at the end
    if os.path.exists(logfile):
        os.remove(logfile)


if __name__ == "__main__":
    first_function()
    print(" ")
    second_function()
    remove_logfile()
