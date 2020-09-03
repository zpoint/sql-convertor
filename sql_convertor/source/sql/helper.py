"""
parse table creation to syntax tree

help:
https://stackoverflow.com/questions/1394998/parsing-sql-with-python

"""
from ..base import BaseHelper


class SQLHelper(BaseHelper):
    def parse_table(self, s, loc, tok):
        tok = self.remove_quotes(s, loc, tok)
        if tok not in self.d_table:
            self.d_table[tok] = dict()
            self.d_curr = self.d_table[tok]
        return tok

    def parse_col(self, s, loc, tok):
        if "cols" not in self.d_curr:
            self.d_curr["cols"] = list()
        ret_dict = dict()
        for i in tok:
            ret_dict.update(i)
        self.d_curr["cols"].append(ret_dict)
        return ret_dict

    def parse_field_name(self, s, loc, tok):
        tok = self.remove_quotes(s, loc, tok)
        return {"field_name": tok}

    def parse_field_type(self, s, loc, tok):
        return {"field_type": tok[0]}

    def parse_field_length(self, s, loc, tok):
        tok = self.get_int(s, loc, tok)
        return {"field_length": tok}

    def parse_field_length_func(self, s, loc, tok):
        tok = self.get_all_int(s, loc, tok)
        return {"field_length": tok}

    def parse_nullable(self, s, loc, tok):
        if tok[0] == "NULL":
            null = True
        else:
            null = False
        return {"null": null}

    def parse_default_value(self, s, loc, tok):
        if isinstance(tok[1], dict) and "field_name" in tok[1]:
            tok = tok[1]["field_name"]
        else:
            tok = tok[1]
        return {"default": tok}

    def parse_comment(self, s, loc, tok):
        return {"comment": "".join(tok[1])}

    def parse_auto_inc(self, s, loc, tok):
        return {"auto_inc": True}

    def parse_table_attr(self, s, loc, tok):
        has_primary = False
        key_name = key_field = None
        for each in tok:
            if each == "PRIMARY":
                has_primary = True
            if isinstance(each, dict):
                if has_primary:
                    self.d_curr["pk"] = each["field_name"]
                elif not key_name:
                    key_name = each["field_name"]
                elif not key_field:
                    key_field = each["field_name"]
        if key_name:
            if "keys" not in self.d_curr:
                self.d_curr["keys"] = dict()
            self.d_curr["keys"][key_name] = key_field
        return {"table_attr": tok}

    def get_int(self, s, loc, tok):
        if tok[0] == "(":
            return tok[1]
        return tok[0]

    def get_all_int(self, s, loc, tok):
        ret_list = list()
        for each in tok:
            if isinstance(each, int):
                ret_list.append(each)
        return ret_list

    def remove_quotes(self, s, loc, tok):
        if tok[0] in ("'", '"', "`"):
            return "".join(tok[1:-1])
        return "".join(tok)

    def parse_table_def(self, s, loc, tok):
        origin_tok = tok
        tok = list(tok)
        equal_index = tok.index("=")
        left = tok[equal_index-1]
        right = tok[equal_index+1]
        self.d_curr[left] = right
        return origin_tok

    def parse_char_set(self, s, loc, tok):
        return {"char_set": tok[0]}
