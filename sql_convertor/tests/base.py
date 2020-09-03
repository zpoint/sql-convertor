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
  `c_is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除',
  `c_statement` VARCHAR(1000) CHARACTER SET UTF8MB4 COLLATE UTF8MB4_BIN DEFAULT '' COMMENT '声明字段',
  `c_record_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录时间',
  PRIMARY KEY (`c_id`),
  KEY `ix_company` (`c_company_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='记录表';

CREATE TABLE `record2` (
  `c_id` INT(64) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  PRIMARY KEY (`c_id`),
  KEY `ix_company` (`c_company_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='记录表';
"""

unittest.TestLoader.sortTestMethodsUsing = None

PEEWEE_COL_LIST = [
    [
        """
            id = peewee.IntegerField(
                    verbose_name="自增主键",
                    null=False,
                    primary_key=True,
                    column_name="c_id")
        """,
        """
            company_id = peewee.CharField(
                max_length=32,
                verbose_name="企业ID",
                null=False,
                column_name="c_company_id")
        """,
        """
            key = peewee.CharField(
                max_length=32,
                verbose_name="KEY",
                null=False,
                default="",
                column_name="c_key")
        """,
        """
            update_dt = peewee.DateTimeField(
                verbose_name="更新时间",
                null=False,
                default=NULL_DATETIME,
                column_name="c_update_dt")
        """,
        """
            update_by = peewee.CharField(
                max_length=32,
                verbose_name="更新用户ID",
                null=False,
                default=NULL_UUID,
                column_name="c_update_by")
        """,
        """
            add_by = peewee.CharField(
                max_length=32,
                verbose_name="创建用户ID",
                null=False,
                default=NULL_UUID,
                column_name="c_add_by")
        """,
        """
            add_dt = peewee.DateTimeField(
                verbose_name="创建时间",
                null=False,
                default=NULL_DATETIME,
                column_name="c_add_dt")
        """,
        """
            is_delete = peewee.BooleanField(
                verbose_name="是否删除",
                null=False,
                default=False,
                column_name="c_is_delete")
        """,
        """
            statement = peewee.CharField(
                max_length=1000,
                verbose_name="声明字段",
                default="",
                column_name="c_statement")
        """,
        """
            record_time = peewee.TimestampField(
                verbose_name="记录时间",
                null=True,
                default=datetime.datetime.now,
                column_name="c_record_time")
        """
    ],
    [
        """
            id = peewee.IntegerField(
                verbose_name="自增主键",
                null=False,
                primary_key=True,
                column_name="c_id")
        """
    ]
]

PEEWEE_META_LIST = [
    """
        class Meta:
            table_name = "record"
            database = db
    """,
    """
        class Meta:
            table_name = "record2"
            database = db
    """
]

PEEWEE_TO_DICT_LIST = [
    """
        def to_dict(self):
            return {
                "id": self.id,
                "company_id": self.company_id,
                "key": self.key,
                "update_dt": self.update_dt,
                "update_by": self.update_by,
                "add_by": self.add_by,
                "add_dt": self.add_dt,
                "is_delete": self.is_delete,
                "statement": self.statement,
                "record_time": self.record_time
            }
    """,
    """
        def to_dict(self):
            return {
                "id": self.id
            }
    """
]
