

import re
import sys


class Regex:
    class NotFound(RuntimeError):
        """Raised when a regex is not found in a string object"""

        def __init__(self, *args: object) -> None:
            super().__init__(*args)

    def __init__(
        self,
        regex_or_pattern: str | re.Pattern,
        *args
    ):
        """
        Initialize the Regex object with a string pattern or a compiled regex pattern.

        :param regex_or_pattern: A string representing the regex pattern or a compiled regex pattern.
        :type regex_or_pattern: str | re.Pattern
        :param args: Additional arguments to pass to the `re.compile` function if `regex_or_pattern` is a string.
        :type args: tuple

        :raises TypeError: If `regex_or_pattern` is not a string or a compiled regex pattern.
        """
        if isinstance(regex_or_pattern, str):
            self.__regex = re.compile(regex_or_pattern, *args)
        elif isinstance(regex_or_pattern, re.Pattern):
            self.__regex = regex_or_pattern
        else:
            raise TypeError("Expected a string or compiled regex pattern")

    def search(self, message: str, pos: int = 0, endpos: int = sys.maxsize) -> re.Match:
        """
        Search for a regex pattern in the given message.

        :param message: The message string to search within.
        :type message: str
        :param pos: The starting position to search within the message.  Defaults to 0 (search from the beginning of the string).
        :type pos: int, optional
        :param endpos: The ending position to search within the message. Defaults to sys.maxsize (search the entire string).
        :type endpos: int, optional

        :return: The first occurence of regex found, as a re.Match object.
        :rtype: re.Match

        :raises Regex.NotFound: If the regex pattern is not found in the message.
        """
        match = self.__regex.search(message, pos, endpos)

        if not match:
            raise Regex.NotFound(
                f"Regex '{self.__regex}' not found in message '{message}'")
        return match

    def find_all(self, message: str, pos: int = 0, endpos: int = sys.maxsize) -> list[str]:
        """
        Find all occurrences of the regex pattern in the given message.

        :param message: The message string to search within.
        :type message: str
        :param pos: The starting position to search within the message.  Defaults to 0 (search from the beginning of the string).
        :type pos: int, optional
        :param endpos: The ending position to search within the message. Defaults to sys.maxsize (search the entire string).
        :type endpos: int, optional

        :return: A list of all matches found. If no matches found, returns an empty list.
        :rtype: list[str]
        """
        match_list = self.__regex.findall(message, pos, endpos)
        if not match_list:
            match_list = []
        return match_list

    def sub(self, repl: str, message: str, count: int = 0) -> str:
        """
        Substitute occurrences of the regex pattern in the given message with a replacement string.

        :param repl: The replacement string.
        :type repl: str
        :param message: The message string to perform substitutions on.
        :type message: str
        :param count: The maximum number of pattern occurrences to be replaced. Defaults to 0 (replace all occurrences).
        :type count: int, optional

        :return: The message string with substitutions made.
        :rtype: str
        """
        result = self.__regex.sub(repl, message, count)
        return result

    def subn(self, repl: str, message: str, count: int = 0) -> tuple[str, int]:
        """
        Substitute occurrences of the regex pattern in the given message with a replacement string and return the number of substitutions made.

        :param repl: The replacement string.
        :type repl: str
        :param message: The message string to perform substitutions on.
        :type message: str
        :param count: The maximum number of pattern occurrences to be replaced. Defaults to 0 (replace all occurrences).
        :type count: int, optional

        :return: A tuple containing the new string with substitutions made and the number of substitutions.
        :rtype: tuple[str, int]
        """
        result, num_subs = self.__regex.subn(repl, message, count)
        return result, num_subs

    @staticmethod
    def compile(pattern: str):
        """
        Compile a regex pattern into a Regex object.

        :param pattern: The regex pattern to compile.
        :type pattern: str

        :return: A Regex object with the compiled pattern.
        :rtype: Regex
        """
        return Regex(pattern)
