import unittest
import os

from unittest.mock import patch

from safethread.thread.utils import ThreadINIFileHandler


class TestINIFileHandler(unittest.TestCase):

    def on_read(self, ini, e):
        self.assertIsNotNone(ini)
        self.assertIsInstance(ini, ThreadINIFileHandler)

        self.assertIsNone(e)

    def on_write(self, ini, e):
        self.assertIsNotNone(ini)
        self.assertIsInstance(ini, ThreadINIFileHandler)

        self.assertIsNone(e)

    def setUp(self):
        self.filename = 'test_config.ini'
        self.ini_handler = ThreadINIFileHandler(
            self.filename,
            on_read=self.on_read,
            on_write=self.on_write
        )

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_init_default_data_not_overloaded(self):
        with self.assertRaises(RuntimeError):
            self.ini_handler._init_default_data()

    def test_set_and_get(self):
        self.ini_handler.set('Config.filename', 'name_of_file')
        self.assertTrue(self.ini_handler.get(
            'Config.filename') == 'name_of_file')

    def test_get_with_fallback(self):
        value = self.ini_handler.get(
            'nonexistent.option', 'default_value')
        self.assertTrue(value == 'default_value')

    def test_show_all(self):
        self.ini_handler.set('section.option', 'value')
        with patch('builtins.print') as mocked_print:
            self.ini_handler.show_all()
            mocked_print.assert_any_call('[section]')
            mocked_print.assert_any_call('option = value')

    def test_read_file_not_found(self):
        def on_read(ini, e):
            self.assertIsNotNone(ini)
            self.assertIsInstance(ini, ThreadINIFileHandler)

            self.assertIsNotNone(e)
            self.assertIsInstance(e, Exception)

        self.ini_handler = ThreadINIFileHandler(
            'nonexistent.ini',
            on_read=on_read
        )

        self.ini_handler.start_read()
        self.ini_handler.join_read()

    def test_write_and_read(self):
        option, section = 'EXAMPLE.optionX', 'value Y'
        self.ini_handler.set(option, section)
        self.ini_handler.start_write()
        self.ini_handler.join_write()

        new_parser = ThreadINIFileHandler(self.filename)
        new_parser.start_read()
        new_parser.join_read()
        self.assertTrue(new_parser.get(option) == section)

    def test_write_and_read_many_times(self):
        # TEST OPTIONS 1 WRITE
        option, section = 'EXAMPLE.optionX', 'value Y'

        self.ini_handler.set(option, section)
        self.ini_handler.start_write()
        self.ini_handler.join_write()

        new_parser = ThreadINIFileHandler(self.filename)
        new_parser.start_read()
        new_parser.join_read()
        self.assertTrue(new_parser.get(option) == section)

        # TEST OPTIONS 2 WRITE
        option_2, section_2 = 'XX.optionzz', 'value AA'

        self.ini_handler.set(option_2, section_2)
        self.ini_handler.start_write()
        self.ini_handler.join_write()

        new_parser.start_read()
        new_parser.join_read()
        self.assertTrue(new_parser.get(option_2) == section_2)


if __name__ == '__main__':
    unittest.main()
