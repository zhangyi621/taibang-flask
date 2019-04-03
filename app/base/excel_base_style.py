import os
from io import BytesIO

import xlwt

from app.base.LogBase import log
from ..constant.constant import constant
from ..util import excel_util


class excel_handle_base(object):
    """
    excel生成对象
    """
    # 不能在成员变量上初始化对象，否则会直接引用内存中已存在的对象

    dir_path: str
    folder_path: str
    file_save_path: str
    file_path: str
    workbook: xlwt.Workbook
    worksheet: xlwt.Worksheet
    data: str
    head_field_list: list
    excel_name: str
    r1: int
    # session_db:object
    statistical_template = {
        # 当前分为2个值，key 、 value

        # key 为唯一 不变，不相加
        # value为相加值
        "A": "key"
    }  # 统计模板

    def __init__(self, data=None, head_field_list=list, excel_name=str, session=None):
        """

        :param session: 数据库链接会话
        :param joinwork: 配置文件类
        :param excel_name: 表总称
        """

        self.user_type = 1
        # 初始列坐标位置
        self.r1 = 0
        # 初始头长度
        self.head_field_list = head_field_list
        # 初始配置文件信息
        # self.joinwork = joinwork
        self.data = data
        # 获取保存路径
        self.dir_path = constant.dbconfig['savePath']
        # 记录表名称
        self.excel_name = excel_name
        # self.session = session
        # 文件路径下的保存目录
        self.folder_path = "%s/" % (self.dir_path)

        # 生成保存路径下文件路径，用于入库；
        self.file_path = "/%s.xls" % (
            excel_name)

        self.file_save_path = self.dir_path + self.file_path

        # 判断指定目录是否存在
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        # 创建 excel
        self.workbook = xlwt.Workbook(encoding="utf-8")
        # 数据库访问会话
        self.session = session()
        self.session.create_mysql()

    def column_width(self, value: object):
        """
        指定单元格列宽
        :param value:
        :return:
        """
        if type(value) is int:
            for i in range(len(self.head_field_list)):
                self.worksheet.col(i).width = value * 20

        if type(value) is list:
            for i in range(len(self.head_field_list)):
                # 如果传入的数组比较短，则跳过，不设定列宽
                self.worksheet.col(i).width = value[i] * 20

    def saves(self):
        self.workbook.save(self.file_save_path)
        log(self.file_save_path)
        return self.file_path

    def bytes(self):

        sio = BytesIO()  # 将获取的数据在内存中写，有时会用到StringIO()
        self.workbook.encoding = 'utf-8'
        self.workbook.save(sio)  # 将文件流保存
        sio.seek(0)  # 光标
        return sio.getvalue()

    def add_sheet(self, sheet_name=str):
        """
        创建 excel 单页
        :param sheet_name: 单页的名称
        :return:None
        """
        self.worksheet = self.workbook.add_sheet(sheet_name)

    def excel_head_title(self, title_name):
        """
        头标题
        :return:
        """

        style = excel_util.title_name_style()

        # 此处表格 r1=0 r2=1 c1=0 c2=8
        self.worksheet.write_merge(self.r1, self.r1 + 1, 0, len(self.head_field_list) - 1, title_name, style)
        self.r1 += 2

    def excel_head_colum_name_list(self):
        """
        字段列表写入
        :return:
        """
        head_list = self.head_field_list

        style = excel_util.interchangeable_style()

        for i in range(len(head_list)):
            self.worksheet.write_merge(self.r1, self.r1, i, i, head_list[i], style)

        self.r1 += 1

    def excel_body_colum_data_single_column(self, r1_main, c1_main, data_field_list_write, is_count_main):
        """
        列表单列的内容写入
        :param c1: 起始写入位置
        :param data_field_list_write: 欲要写入数据的数组
        :param is_count_main: 是否开启总统计，小计位置时必须开启
        :return:
        """
        for index in range(len(data_field_list_write)):
            c1 = index + c1_main
            key = chr(ord("A") + c1)

            # 取通用样式
            style = excel_util.interchangeable_style()
            # 写入数据
            self.worksheet.write_merge(r1_main, r1_main, c1, c1, data_field_list_write[index], style)

            # 写入统计
            value = self.count_son.get(key)
            # 判断统计类型，False=只进行子统计，True=总统计

            if value is None or type(value) == str and len(value) == 0:
                # 如果为空或者空字符串不统计
                continue
            else:
                if is_count_main:
                    # 加入总统计
                    self.count_main[key] += data_field_list_write[index]
                else:
                    # 加入子统计
                    self.count_son[key] += data_field_list_write[index]
