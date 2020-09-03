HINT_TEXT = "Code of this model is auto generated from SQL, " \
            "if you need help please reach github.com/zpoint/sql-convertor"
HINT_TEXT_CN = "本段代码由程序从SQL建表语句自动生成, 需要帮助请访问 github.com/zpoint/sql-convertor"

field_type_map = {
    "VARCHAR": "CharField",
    "INT": "IntegerField",
    "TINYINT": "SmallIntegerField",
    "SMALLINT": "SmallIntegerField",
    "CHAR": "CharField",
    "DATE": "DateField",
    "DATETIME": "DateTimeField",
    "DECIMAL": "DecimalField",
    "TEXT": "TextField",
    "BLOB": "TextField",
    "TIMESTAMP": "TimestampField"
}
default_map = {
    "00000000000000000000000000000000": "NULL_UUID",
    "1970-01-01 00:00:00": "NULL_DATETIME"
}


class Dest(object):
    def __init__(self, sql_table_dict: dict, lower_case=True, indent="    ",
                 base_model_name="BaseModel", hint_text="CN"):
        self.sql_table_dict = sql_table_dict
        self.lower_case = lower_case
        self.br = "\n"
        self.indent = indent
        self.current_indent = self.next_indent = ""
        self.base_model_name = base_model_name
        self.key_list = list()
        self.pk = None
        self.hint_text = HINT_TEXT_CN if hint_text == "CN" else HINT_TEXT
        self.default_map = default_map
        self.field_type_map = field_type_map

    def emit_row(self, row_dict: dict) -> str:
        """
        :param row_dict: {'field_name': 'C_ID', 'field_type': 'INT', 'field_length': 64, 'null': False,
        'auto_inc': True, 'comment': '自增主键'}
        :return: str
        """
        raise NotImplementedError

    def emit(self) -> str:
        raise NotImplementedError

    def strip_key_func(self, key: str) -> str:
        if self.lower_case:
            key = key.lower()
        if key.startswith("c_"):
            key = key[2:]
        return key

    def forward_indent(self):
        if not self.next_indent:
            self.next_indent = self.indent
        self.current_indent = self.next_indent
        self.next_indent = self.current_indent + self.indent

    def backward_indent(self):
        self.current_indent = self.current_indent[:-len(self.indent)]
        self.next_indent = self.next_indent[:-len(self.indent)]

    def reset_indent(self):
        self.current_indent = self.next_indent = ""

    @staticmethod
    def strip_table_func(key: str) -> str:
        if key.startswith("t_"):
            key = key[2:]
        ret_key = ""
        key = key.split("_")
        for each in key:
            ret_key += each[0].upper()
            ret_key += each[1:]
        return ret_key

    def get_pk(self, table_dict):
        if "pk" in table_dict and table_dict["pk"]:
            self.pk = self.strip_key_func(table_dict["pk"])
            return
        self.pk = None

    def set_default_map(self, default_map: dict):
        self.default_map = default_map

    def set_field_type_map(self, field_type_map: dict):
        self.field_type_map = field_type_map
