import time
import unittest
import os
import logging

from safethread.thread.utils import ThreadLog, ThreadSingleton

global log_instance

logfile = "test_log.log"


def tearDownModule():
    # Perform cleanup actions here (e.g., remove temp files, close DB connections)
    log_instance.__del__()
    if os.path.exists(logfile):
        os.remove(logfile)
    print("All tests in this module have finished.")


class TestLog(unittest.TestCase):
    logfile = logfile
    log_level = ThreadLog.INFO
    log_format = "%(asctime)s - [%(levelname)s] - %(name)s.%(funcName)s(): %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    def __create_log_instance(self):
        global log_instance
        log_instance = ThreadLog.get_instance(
            logfile=self.logfile,
            log_level=self.log_level,
            log_format=self.log_format,
            date_format=self.date_format,
        )

    def setUp(self):
        self.__create_log_instance()

    def test_log_instances(self):
        instance1 = log_instance
        self.__create_log_instance()
        instance2 = log_instance
        self.assertEqual(instance1, instance2)
        self.assertIsInstance(instance1, ThreadSingleton)
        self.assertIsInstance(instance2, ThreadSingleton)

    def test_logger_instances(self):
        instance1 = log_instance.get_logger("test_logger")
        instance2 = log_instance.get_logger("test_logger")
        self.assertEqual(instance1, instance2)

    def test_log_level(self):
        self.assertEqual(log_instance.get_level(), self.log_level)

    def test_log_format(self):
        self.assertEqual(log_instance.get_log_format(), self.log_format)

    def test_date_format(self):
        self.assertEqual(log_instance.get_date_format(), self.date_format)

    def test_get_logger(self):
        logger_name = "test_logger"
        logger = log_instance.get_logger(logger_name)
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, logger_name)

    def test_log_message(self):
        msg = "This is a test log message."

        logger = log_instance.get_logger("test_logger")
        logger.info(msg)
        log_instance.flush_logs_from(logger.name)
        time.sleep(0.1)

        self.assertTrue(os.path.exists(self.logfile))
        with open(self.logfile, "r") as f:
            log_content = f.read()
        self.assertIn(msg, log_content)


if __name__ == "__main__":
    unittest.main()
