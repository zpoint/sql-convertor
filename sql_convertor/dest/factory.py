from collections import defaultdict
from .peewee import PeeWeeOutPut
from .base import Dest
from sql_convertor.source.base import BaseParser

OriginTypeMap = {
    "peewee": PeeWeeOutPut
}
TypeMap = defaultdict(None)
TypeMap.update(OriginTypeMap)


class OutPutFactory(object):
    @staticmethod
    def create_output(type_str: str, parser: BaseParser) -> Dest:
        output_cls = TypeMap[type_str]
        if output_cls is None:
            raise NotImplementedError("unsupported type: %s" % (type_str, ))
        return output_cls(parser.get_table())

    @staticmethod
    def list_all():
        return [i for i in TypeMap.keys()]
