from sql_convertor.source.sql.parser import SQLParser
from sql_convertor.dest.peewee import PeeWeeOutPut

sampleSQL = """CREATE TABLE `t_record` (
  `c_id` INT(64) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  PRIMARY KEY (`c_id`),
  KEY `ix_company` (`c_company_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='记录表';
"""
parser = SQLParser()
parser.parse_string(sampleSQL)
output = PeeWeeOutPut(parser.get_table())
r = output.emit()
print(r)
