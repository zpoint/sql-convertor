from pyparsing import (
    Literal,
    Word,
    delimitedList,
    alphas,
    alphanums,
    OneOrMore,
    Optional,
    quotedString,
    removeQuotes,
    pyparsing_common
)
from .helper import SQLHelper
from ..base import BaseParser


class SQLParser(BaseParser):
    def generate_parser(self):
        # tablename
        word = Word(alphas, alphanums + "_")
        keyword = ("`" + word + "`") | word
        keyword = keyword.setParseAction(self.helper.remove_quotes)
        string_literal = quotedString.setParseAction(removeQuotes)
        number = pyparsing_common.number()

        # column
        type_ = Literal("CHAR") | Literal("VARCHAR") | Literal("TINYTEXT") | Literal("TEXT") | \
                Literal("MEDIUMTEXT") | Literal("LONGTEXT") | Literal("TINYINT") | Literal("SMALLINT") | \
                Literal("MEDIUMINT") | Literal("INT") | Literal("BIGINT") | Literal("FLOAT") | Literal("DOUBLE") | \
                Literal("DECIMAL") | Literal("DATETIME") | Literal("DATE") | Literal("TIMESTAMP") | Literal("TIME") | \
                Literal("ENUM") | Literal("SET") | Literal("BLOB")
        enclosing_int = "(" + number + ")"
        enclosing_func = "(" + number + OneOrMore("," + number) + ")"
        enclosing_keyword = "(" + OneOrMore(keyword) + ")"
        char_set = Literal("CHARACTER SET") + word + Optional(Literal("COLLATE") + word)
        nullable = Literal("NOT NULL") | Literal("NULL")
        default = Literal("DEFAULT") + (string_literal | number | Literal("NULL") | keyword)
        comment = Literal("COMMENT") + string_literal
        auto_inc = Literal("AUTO_INCREMENT")

        enclosing_int.setParseAction(self.helper.parse_field_length)
        enclosing_func.setParseAction(self.helper.parse_field_length_func)
        keyword.setParseAction(self.helper.parse_field_name)
        char_set.setParseAction(self.helper.parse_char_set)
        type_.setParseAction(self.helper.parse_field_type)
        nullable.setParseAction(self.helper.parse_nullable)
        auto_inc.setParseAction(self.helper.parse_auto_inc)
        default.setParseAction(self.helper.parse_default_value)
        comment.setParseAction(self.helper.parse_comment)
        #   `c_add_dt` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
        col_stm = keyword + type_ + Optional(enclosing_int | enclosing_func) + Optional(nullable) + Optional(auto_inc) + Optional(char_set) + Optional(default) + Optional(comment)
        col_stm.setParseAction(self.helper.parse_col)

        # key
        using_stm = Literal("USING") + word
        key = Optional(Literal("PRIMARY")) + Literal("KEY") + Optional(keyword) + enclosing_keyword
        key.setParseAction(self.helper.parse_table_attr)
        key_stm = key + Optional(using_stm)

        cols_def = delimitedList(col_stm | key_stm)

        # table
        origin_keyword = ("`" + word + "`") | word
        single_table_def = OneOrMore(origin_keyword) + "=" + (origin_keyword | string_literal | number)
        single_table_def.setParseAction(self.helper.parse_table_def)
        table_def = OneOrMore(single_table_def)

        table_name = ("`" + word + "`") | word
        table_name = table_name.setParseAction(self.helper.remove_quotes)
        table_name.setParseAction(self.helper.parse_table)
        create_table_def = (
                Literal("CREATE")
                + "TABLE"
                + table_name.setResultsName("tablename")
                + "("
                + cols_def.setResultsName("columns")
                + ")"
                + table_def.setResultsName("tabledef")
                + ";"
        )

        statement_def = create_table_def
        # defs = OneOrMore(statement_def)
        # self.defs = defs
        self.defs = statement_def

    def _get_helper(self):
        return SQLHelper(self.d_table, self.d_curr)
