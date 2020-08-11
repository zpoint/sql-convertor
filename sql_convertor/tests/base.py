import unittest
from sql_convertor import ParserFactory, OutPutFactory

sampleSQL = """CREATE TABLE `record` (
  `c_id` INT(64) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `c_company_id` varchar(32) NOT NULL COMMENT '企业Id',
  `c_key` varchar(32) NOT NULL DEFAULT "" COMMENT 'key',
  `c_update_dt` datetime NOT NULL DEFAULT "1970-01-01 00:00:00" COMMENT '更新时间',
  `c_update_by` varchar(32) NOT NULL DEFAULT '00000000000000000000000000000000' COMMENT '更新用户id',
  `c_add_by` varchar(32) NOT NULL DEFAULT '00000000000000000000000000000000' COMMENT '创建用户id',
  `c_add_dt` datetime NOT NULL DEFAULT "1970-01-01 00:00:00" COMMENT '创建时间',
  `c_is_delete` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除',
  PRIMARY KEY (`c_id`),
  KEY `ix_company` (`c_company_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='记录表';
"""

unittest.TestLoader.sortTestMethodsUsing = None
