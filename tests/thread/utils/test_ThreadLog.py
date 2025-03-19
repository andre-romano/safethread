import time
import unittest
import os
import logging

from safethread.thread.utils import ThreadLog, ThreadSingleton


class TestLog(unittest.TestCase):
    LOGFILE = "test_log.log"
    log_level = ThreadLog.INFO
    log_format = "%(asctime)s - [%(levelname)s] - %(name)s.%(funcName)s(): %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def tearDownClass(cls):
        try:
            logging.shutdown()
            while True:
                try:
                    os.remove(TestLog.LOGFILE)
                    break
                except:
                    time.sleep(0.1)
        except:
            pass

    def setUp(self):
        self.log_instance = self.__create_log_instance()

    def __create_log_instance(self):
        return ThreadLog.get_instance(
            logfile=self.LOGFILE,
            log_level=self.log_level,
            log_format=self.log_format,
            date_format=self.date_format,
        )

    def test_log_instances(self):
        instance1 = self.__create_log_instance()
        instance2 = self.__create_log_instance()
        self.assertTrue(instance1 == instance2)
        self.assertIsInstance(instance1, ThreadSingleton)
        self.assertIsInstance(instance2, ThreadSingleton)

    def test_logger_instances(self):
        instance1 = self.log_instance.get_logger("test_logger")
        instance2 = self.log_instance.get_logger("test_logger")
        self.assertTrue(instance1 == instance2)

    def test_log_level(self):
        self.assertTrue(self.log_instance.get_level() == self.log_level)

    def test_log_format(self):
        self.assertTrue(self.log_instance.get_log_format() == self.log_format)

    def test_date_format(self):
        self.assertTrue(self.log_instance.get_date_format()
                        == self.date_format)

    def test_get_logger(self):
        logger_name = "test_logger"
        logger = self.log_instance.get_logger(logger_name)
        self.assertIsInstance(logger, logging.Logger)
        self.assertTrue(logger.name == logger_name)

    def test_log_message(self):
        msg = "This is a test log message."

        logger = self.log_instance.get_logger("test_logger")
        logger.info(msg)
        self.log_instance.flush_logs_from(logger.name)
        time.sleep(0.1)

        self.assertTrue(os.path.exists(self.LOGFILE))
        with open(self.LOGFILE, "r") as f:
            log_content = f.read()
        self.assertIn(msg, log_content)


if __name__ == "__main__":
    unittest.main()
