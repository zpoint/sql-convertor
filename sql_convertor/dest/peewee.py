import re
from .base import Dest


class PeeWeeOutPut(Dest):
    def emit(self) -> str:
        ret_str = ""
        for table_name, table_dict in self.sql_table_dict.items():
            self.key_list.clear()
            # print(f"{table_name} {table_dict}")
            self.get_pk(table_dict)
            if self.lower_case:
                table_name = table_name.lower()

            self.reset_indent()
            ret_str += self.emit_table_cls(table_name)
            self.forward_indent()
            for col in table_dict["cols"]:
                ret_str += self.emit_row(col)
            ret_str += self.emit_table_meta(table_name)
            ret_str += self.emit_to_dict()
            self.backward_indent()
        return ret_str

    def emit_row(self, row_dict: dict) -> str:
        default = None
        default_set = False
        if "default" in row_dict:
            default = row_dict["default"]

        key = self.strip_key_func(row_dict["field_name"])
        self.key_list.append(key)
        if row_dict["field_type"] == "TINYINT" and row_dict["field_length"] == 1:
            field_type = "BooleanField"
            if default is not None:
                # row_dict["default"] = re.sub('`"\'', '', row_dict["default"])
                default = repr(bool(int(row_dict["default"])))
                default_set = True
        else:
            field_type = self.field_type_map[row_dict["field_type"]]
        if isinstance(default, str) and not default_set:
            # TODO 默认值预处理搬到 parse 层处理, 而不是 emit 层处理
            if default == "NULL":
                default = str(None)
                if "null" not in row_dict:
                    row_dict["null"] = "True"
            elif default in self.default_map:
                default = self.default_map[default]
            elif default.isdigit():
                if field_type in ("IntegerField", "SmallIntegerField"):
                    default = int(default)
                else:
                    default = "\"" + default + "\""
            elif default == "CURRENT_TIMESTAMP":
                default = "datetime.datetime.now"
            else:
                default = "\"%s\"" % (default, )

        ret_str = self.indent + "%s = peewee.%s(%s" % (key, field_type, self.br)
        # max_length
        if field_type == "CharField" and "field_length" in row_dict:
            ret_str += self.next_indent + "max_length=%s,%s" % (row_dict["field_length"], self.br)
        # verbose_name
        if "comment" in row_dict:
            ret_str += self.next_indent + "verbose_name=\"%s\",%s" % (row_dict["comment"], self.br)
        # null
        if "null" in row_dict:
            ret_str += self.next_indent + "null=%s,%s" % (repr(bool(row_dict["null"])), self.br)
        # default
        if default is not None:
            ret_str += self.next_indent + "default=%s,%s" % (default, self.br)
        if key == self.pk:
            ret_str += self.next_indent + "primary_key=%s,%s" % (repr(True), self.br)
        # column_name
        ret_str += self.next_indent + "column_name=\"%s\")%s" % (row_dict["field_name"].lower(), self.br*2)
        return ret_str

    def emit_table_cls(self, table_name):
        table_name = self.strip_table_func(table_name)
        ret_str = "class %s(%s):%s\"\"\"%s\"\"\"%s" % (
            table_name, self.base_model_name, self.br+self.indent, self.hint_text, self.br
        )
        return ret_str

    def emit_table_meta(self, table_name):
        ret_str = "%sclass Meta:%s" % (self.current_indent, self.br)
        ret_str += "%s%s = \"%s\"%s" % (self.next_indent, "table_name", table_name, self.br)
        ret_str += "%s%s = %s%s" % (self.next_indent, "database", "db", self.br*2)
        return ret_str

    def emit_to_dict(self):
        ret_str = "%sdef to_dict(self):%s" % (self.current_indent, self.br)
        ret_str += "%sreturn {%s" % (self.next_indent, self.br)
        for key in self.key_list:
            ret_str += '%s"%s": self.%s,%s' % (self.next_indent+self.indent, key, key, self.br)
        ret_str = ret_str[:-2]
        ret_str += "%s%s%s" % (self.br, self.next_indent + "}", self.br*2)
        return ret_str
