import logging
import time
import unittest
import os
import tracemalloc


from unittest.mock import patch

from safethread.thread.utils import ThreadINIFileHandler


class TestINIFileHandler(unittest.TestCase):
    @staticmethod
    def create_file(filename):
        try:
            with open(filename, 'x') as file:
                pass
        except:
            pass

    @staticmethod
    def remove_file(filename):
        """Cleanup after all tests in the class have finished."""
        while os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                time.sleep(0.1)

    def on_read(self, ini, e):
        self.assertIsNotNone(ini)
        self.assertIsInstance(ini, ThreadINIFileHandler)

        self.assertIsNone(e)

    def on_write(self, ini, e):
        self.assertIsNotNone(ini)
        self.assertIsInstance(ini, ThreadINIFileHandler)

        self.assertIsNone(e)

    def test_init_default_data_not_overloaded(self):
        test_file = "test_file1.ini"
        ini_handler = ThreadINIFileHandler(
            test_file,
            on_read=self.on_read,
            on_write=self.on_write
        )

        with self.assertRaises(RuntimeError):
            ini_handler._init_default_data()

    def test_set_and_get(self):
        test_file = "test_file2.ini"
        ini_handler = ThreadINIFileHandler(
            test_file,
            on_read=self.on_read,
            on_write=self.on_write
        )
        ini_handler.set('Config.FILENAME', 'name_of_file')
        self.assertTrue(ini_handler.get(
            'Config.FILENAME') == 'name_of_file')

    def test_get_with_fallback(self):
        test_file = "test_file3.ini"
        ini_handler = ThreadINIFileHandler(
            test_file,
            on_read=self.on_read,
            on_write=self.on_write
        )
        value = ini_handler.get(
            'nonexistent.option', 'default_value')
        self.assertTrue(value == 'default_value')

    def test_show_all(self):
        test_file = "test_file4.ini"
        ini_handler = ThreadINIFileHandler(
            test_file,
            on_read=self.on_read,
            on_write=self.on_write
        )
        ini_handler.set('section.option', 'value')
        with patch('builtins.print') as mocked_print:
            ini_handler.show_all()
            mocked_print.assert_any_call('[section]')
            mocked_print.assert_any_call('option = value')

    def test_read_file_not_found(self):
        def on_read(ini, e):
            self.assertIsNotNone(ini)
            self.assertIsInstance(ini, ThreadINIFileHandler)

            self.assertIsNotNone(e)
            self.assertIsInstance(e, Exception)

        ini_handler = ThreadINIFileHandler(
            'nonexistent.ini',
            on_read=on_read
        )

        ini_handler.start_read()
        ini_handler.join_read()

    def test_write_and_read(self):
        test_file = "test_file5.ini"
        ini_handler = ThreadINIFileHandler(
            test_file,
            on_read=self.on_read,
            on_write=self.on_write
        )

        option, section = 'EXAMPLE.optionx', 'value Y'
        ini_handler.set(option, section)
        ini_handler.start_write()
        ini_handler.join_write()

        new_parser = ThreadINIFileHandler(test_file)
        new_parser.start_read()
        new_parser.join_read()
        new_parser.show_all()
        logging.info(new_parser.get(option))
        self.assertTrue(new_parser.get(option) == section)

        self.remove_file(test_file)

    def test_write_and_read_many_times(self):
        test_file = "test_file6.ini"
        ini_handler = ThreadINIFileHandler(
            test_file,
            on_read=self.on_read,
            on_write=self.on_write
        )

        # TEST OPTIONS 1 WRITE
        option, section = 'EXAMPLE.optionX', 'value Y'

        ini_handler.set(option, section)
        ini_handler.start_write()
        ini_handler.join_write()

        new_parser = ThreadINIFileHandler(test_file)
        new_parser.start_read()
        new_parser.join_read()
        self.assertTrue(new_parser.get(option) == section)

        # TEST OPTIONS 2 WRITE
        option_2, section_2 = 'XX.option', 'value AA'

        ini_handler.set(option_2, section_2)
        ini_handler.start_write()
        ini_handler.join_write()

        new_parser.start_read()
        new_parser.join_read()
        self.assertTrue(new_parser.get(option_2) == section_2)

        self.remove_file(test_file)


if __name__ == '__main__':
    tracemalloc.start()
    unittest.main()
