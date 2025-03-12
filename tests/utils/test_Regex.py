import unittest

from safethread.utils import Regex


class TestRegex(unittest.TestCase):

    def test_search_found(self):
        regex = Regex(r'\d+')
        message = "There are 123 numbers here"
        match = regex.search(message)
        self.assertEqual(match.group(), '123')

    def test_search_not_found(self):
        regex = Regex(r'\d+')
        message = "No numbers here"
        with self.assertRaises(Regex.NotFound):
            regex.search(message)

    def test_find_all(self):
        regex = Regex(r'\d+')
        message = "Numbers: 123, 456, 789"
        matches = regex.find_all(message)
        self.assertEqual(matches, ['123', '456', '789'])

    def test_find_all_empty(self):
        regex = Regex(r'\d+')
        message = "No numbers here"
        matches = regex.find_all(message)
        self.assertEqual(matches, [])

    def test_sub(self):
        regex = Regex(r'\d+')
        message = "Replace 123 with numbers"
        result = regex.sub('numbers', message)
        self.assertEqual(result, "Replace numbers with numbers")

    def test_subn(self):
        regex = Regex(r'\d+')
        message = "Replace 123 and 456 with numbers"
        result, num_subs = regex.subn('numbers', message)
        self.assertEqual(result, "Replace numbers and numbers with numbers")
        self.assertEqual(num_subs, 2)

    def test_compile(self):
        pattern = r'\d+'
        regex = Regex.compile(pattern)
        self.assertIsInstance(regex, Regex)
        self.assertEqual(
            regex._Regex__regex.pattern,  # type: ignore
            pattern
        )


if __name__ == '__main__':
    unittest.main()
