import os
import sys
import argparse
from argparse import RawTextHelpFormatter
from sql_convertor.source import ParserFactory
from sql_convertor.dest import OutPutFactory


class Args(object):
    from_desc = "argument 'from' can only set to one of %s" % (ParserFactory.list_all(), )
    to_desc = "argument 'to' can only set to one of %s" % (OutPutFactory.list_all(), )
    source_desc = "filepath 'a.sql' or code"
    dest_desc = "output filepath 'out.sql', default to stdout"


def get_args():
    parser = argparse.ArgumentParser(
        prog="convert",
        formatter_class=RawTextHelpFormatter,
        description="""
convert SQL table definition to peewee/django/... model definition, or convert model definition to SQL table
                    
example:
    %convertor sql peewee 1.sql
    %convertor sql peewee 1.sql out.py
    %convertor sql peewee "CREATE TABLE \\`t_record\\` ( \\
    \\`c_id\\` INT(64) NOT NULL AUTO_INCREMENT COMMENT '自增主键', \\
    PRIMARY KEY (\\`c_id\\`), \\
    KEY \\`ix_company\\` (\\`c_company_id\\`) USING BTREE \\
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='记录表';"
    """,
    )
    parser.add_argument("from", choices=ParserFactory.list_all(), help=Args.from_desc, type=str.lower,
                        default=ParserFactory.list_all()[0])
    parser.add_argument("to", choices=OutPutFactory.list_all(), help=Args.to_desc, type=str.lower,
                        default=OutPutFactory.list_all()[0])
    parser.add_argument("source", help=Args.source_desc, type=str.lower)
    parser.add_argument("dest", help=Args.dest_desc, default="", nargs="?", type=str.lower)
    return parser.parse_args()


def main():
    args = get_args()
    sql_parser = ParserFactory.create_parser(getattr(args, "from"))
    source = args.source
    if os.path.isfile(source):
        sql_parser.parse_file(source)
    else:
        sql_parser.parse_string(source)
    output_instance = OutPutFactory.create_output(args.to, sql_parser)

    result = output_instance.emit()
    # write to destination
    dest = args.dest
    if dest:
        with open(dest, "w") as f:
            f.write(result)
    else:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
