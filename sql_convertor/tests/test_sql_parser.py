from .base import ParserFactory, sampleSQL


class TestSQLParser(object):
    field_name_row_map = dict()

    @classmethod
    def setup_class(cls):
        cls.parser = ParserFactory.create_parser("sql")
        cls.parser.parse_string(sampleSQL)

    def test_parse(self):
        table = self.parser.get_table()
        assert "RECORD" in table
        record = table["RECORD"]
        assert "cols" in record
        for col in record["cols"]:
            self.field_name_row_map[col["field_name"]] = col

    def test_c_id(self):
        assert "C_ID" in self.field_name_row_map
        assert self.field_name_row_map["C_ID"] == {
            'field_name': 'C_ID', 'field_type': 'INT', 'field_length': 64, 'null': False, 'auto_inc': True,
            'comment': '自增主键'
        }

    def test_c_company_id(self):
        assert "C_COMPANY_ID" in self.field_name_row_map
        assert self.field_name_row_map["C_COMPANY_ID"] == {
            'field_name': 'C_COMPANY_ID', 'field_type': 'VARCHAR', 'field_length': 32, 'null': False,
            'comment': '企业ID'
        }

    def test_c_key(self):
        assert "C_KEY" in self.field_name_row_map
        assert self.field_name_row_map["C_KEY"] == {
            'field_name': 'C_KEY', 'field_type': 'VARCHAR', 'field_length': 32, 'null': False,
            'default': '', 'comment': 'KEY'
        }

    def test_c_update_dt(self):
        assert "C_UPDATE_DT" in self.field_name_row_map
        assert self.field_name_row_map["C_UPDATE_DT"] == {
            'field_name': 'C_UPDATE_DT', 'field_type': 'DATETIME', 'null': False, 'default': '1970-01-01 00:00:00',
            'comment': '更新时间'
        }

    def test_c_update_by(self):
        assert "C_UPDATE_BY" in self.field_name_row_map
        assert self.field_name_row_map["C_UPDATE_BY"] == {
            'field_name': 'C_UPDATE_BY', 'field_type': 'VARCHAR', 'field_length': 32, 'null': False,
            'default': '00000000000000000000000000000000', 'comment': '更新用户ID'
        }

    def test_c_add_by(self):
        assert "C_ADD_BY" in self.field_name_row_map
        assert self.field_name_row_map["C_ADD_BY"] == {
            'field_name': 'C_ADD_BY', 'field_type': 'VARCHAR', 'field_length': 32, 'null': False,
            'default': '00000000000000000000000000000000', 'comment': '创建用户ID'
        }

    def test_c_add_dt(self):
        assert "C_ADD_DT" in self.field_name_row_map
        assert self.field_name_row_map["C_ADD_DT"] == {
            'field_name': 'C_ADD_DT', 'field_type': 'DATETIME', 'null': False, 'default': '1970-01-01 00:00:00',
            'comment': '创建时间'
        }

    def test_c_is_delete(self):
        assert "C_IS_DELETE" in self.field_name_row_map
        assert self.field_name_row_map["C_IS_DELETE"] == {
            'field_name': 'C_IS_DELETE', 'field_type': 'TINYINT', 'field_length': 1, 'null': False,
            'default': '0', 'comment': '是否删除'
        }

    def test_c_statement(self):
        assert "C_STATEMENT" in self.field_name_row_map
        assert self.field_name_row_map["C_STATEMENT"] == {
            'char_set': 'CHARACTER SET', 'comment': '声明字段', 'default': '', 'field_length': 1000,
            'field_name': 'C_STATEMENT', 'field_type': 'VARCHAR'
        }

    def test_c_record_time(self):
        assert "C_RECORD_TIME" in self.field_name_row_map
        assert self.field_name_row_map["C_RECORD_TIME"] == {
            'comment': '记录时间', 'default': 'CURRENT_TIMESTAMP', 'field_name': 'C_RECORD_TIME',
            'field_type': 'TIMESTAMP', 'null': True
        }
