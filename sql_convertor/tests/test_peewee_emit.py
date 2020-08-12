from .base import ParserFactory, OutPutFactory, sampleSQL


class TestPeeWeeEmit(object):
    @classmethod
    def setup_class(cls):
        cls.parser = ParserFactory.create_parser("sql")
        cls.parser.parse_string(sampleSQL)
        cls.outputer = OutPutFactory.create_output("peewee", cls.parser)

    def test_emit(self):
        # TODO 重写成按行测试
        res = self.outputer.emit()
        assert res == 'class Record(BaseModel):\n    """本段代码由程序从SQL建表语句自动生成, 需要帮助请联系 zp0int@qq.com"""\n    id = peewee.IntegerField(\n        verbose_name="自增主键",\n        null=False,\n        primary_key=True,\n        column_name="c_id")\n\n    company_id = peewee.CharField(\n        verbose_name="企业ID",\n        null=False,\n        column_name="c_company_id")\n\n    key = peewee.CharField(\n        verbose_name="KEY",\n        null=False,\n        default="",\n        column_name="c_key")\n\n    update_dt = peewee.DateTimeField(\n        verbose_name="更新时间",\n        null=False,\n        default=NULL_DATETIME,\n        column_name="c_update_dt")\n\n    update_by = peewee.CharField(\n        verbose_name="更新用户ID",\n        null=False,\n        default=NULL_UUID,\n        column_name="c_update_by")\n\n    add_by = peewee.CharField(\n        verbose_name="创建用户ID",\n        null=False,\n        default=NULL_UUID,\n        column_name="c_add_by")\n\n    add_dt = peewee.DateTimeField(\n        verbose_name="创建时间",\n        null=False,\n        default=NULL_DATETIME,\n        column_name="c_add_dt")\n\n    is_delete = peewee.BooleanField(\n        verbose_name="是否删除",\n        null=False,\n        default=False,\n        column_name="c_is_delete")\n\n    class Meta:\n        table_name = "record"\n        database = db\n\n    def to_dict(self):\n        return {\n            "id": self.id,\n            "company_id": self.company_id,\n            "key": self.key,\n            "update_dt": self.update_dt,\n            "update_by": self.update_by,\n            "add_by": self.add_by,\n            "add_dt": self.add_dt,\n            "is_delete": self.is_delete\n        }\n\n'
