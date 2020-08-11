from collections import defaultdict
from .sql.parser import SQLParser
from .base import BaseParser

OriginTypeMap = {
    "sql": SQLParser
}
TypeMap = defaultdict(None)
TypeMap.update(OriginTypeMap)


class ParserFactory(object):
    @staticmethod
    def create_parser(type_str: str) -> BaseParser:
        parser_cls = TypeMap[type_str]
        if parser_cls is None:
            raise NotImplementedError("unsupported type: %s" % (type_str, ))
        return parser_cls()

    @staticmethod
    def list_all():
        return [i for i in TypeMap.keys()]
