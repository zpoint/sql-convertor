import re
from .base import ParserFactory, OutPutFactory, sampleSQL, PEEWEE_COL_LIST, PEEWEE_META_LIST, PEEWEE_TO_DICT_LIST
from ..dest.peewee import PeeWeeOutPut


class TestPeeWeeEmit(object):
    @classmethod
    def setup_class(cls):
        cls.parser = ParserFactory.create_parser("sql")
        cls.parser.parse_string(sampleSQL)
        cls.outputer: PeeWeeOutPut = OutPutFactory.create_output("peewee", cls.parser)

    def test_emit(self):
        index = 0
        assert_table_name = ["record", "record2"]
        for table_name, table_dict in self.outputer.sql_table_dict.items():
            self.outputer.key_list.clear()
            # print(f"{table_name} {table_dict}")
            self.outputer.get_pk(table_dict)
            if self.outputer.lower_case:
                table_name = table_name.lower()
            self.outputer.reset_indent()
            self.outputer.forward_indent()
            assert table_name == assert_table_name[index]
            self.assert_table_one(table_dict["cols"], PEEWEE_COL_LIST[index])
            meta_result = self.outputer.emit_table_meta(table_name)
            print(f"{meta_result}")
            print(f"{PEEWEE_META_LIST[index]}")
            assert self.strip_space(meta_result) == self.strip_space(PEEWEE_META_LIST[index])
            to_dict_result = self.outputer.emit_to_dict()
            assert self.strip_space(to_dict_result) == self.strip_space(PEEWEE_TO_DICT_LIST[index])
            self.outputer.backward_indent()
            index += 1

    def assert_table_one(self, cols, assert_results):
        for index, col in enumerate(cols):
            row_result = self.outputer.emit_row(col)
            assert self.strip_space(row_result) == self.strip_space(assert_results[index])

    def strip_space(self, text):
        return re.sub("\\s+", " ", text)
