import abc
from pyparsing import ParseElementEnhance


class BaseHelper(metaclass=abc.ABCMeta):
    def __init__(self, d_table: dict, d_curr: dict):
        self.d_table = d_table
        self.d_curr = d_curr


class BaseParser(metaclass=abc.ABCMeta):
    def __init__(self):
        self.d_table: dict = dict()
        self.d_curr: dict = dict()
        self.helper = self._get_helper()
        self.defs: ParseElementEnhance = None
        self.generate_parser()

    def parse_string(self, string: str):
        string = string.upper()
        for match in self.defs.searchString(string):
            # already handled by helper
            pass

    def parse_file(self, filename: str):
        with open(filename, "r") as f:
            string = f.read()
        self.parse_string(string)

    def generate_parser(self):
        raise NotImplemented

    def get_table(self, clear=True) -> dict:
        if not self.d_table:
            raise ValueError("Please call parse_string/parse_file before call get_table")
        ret_table = self.d_table
        if clear:
            self.d_table = dict()
            self.d_curr = dict()
        return ret_table

    def _get_helper(self):
        return BaseHelper(self.d_table, self.d_curr)
