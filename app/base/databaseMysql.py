from app.base.LogBase import log
from app.constant import constant
import pymysql


class session_db(object):
    port: int
    host: str
    username: str
    password: str
    db: str

    def __init__(self):
        self.host = constant.constant.dbconfig["host"]
        self.username = constant.constant.dbconfig['username']
        self.password = constant.constant.dbconfig['password']
        self.db = constant.constant.dbconfig['db']

        self.port = constant.constant.dbconfig['port'] or 3306

    def __del__(self):
        """
        指定当前对象被销毁前操作内容
        :return:
        """
        try:
            self.pymysql.close()
            # 成功关闭数据库链接
            log("close mysql tcp")
        except AttributeError as e:
            # 未创建 数据库链接
            log("not create mysql tcp")
        except pymysql.err.Error as e:
            # 已关闭
            log("mysql tpc closed")

    def create_mysql(self):

        host = self.host
        username = self.username
        password = self.password
        db = self.db
        log("create mysql tcp Host:%s ,username:%s,db:%s" % (host, username, db))
        self.pymysql = pymysql.connect(host=host, user=username, password=password, database=db, port=self.port)
        log("create mysql success")
        return self.pymysql

    def execute_by_fetchall(self, sql):
        """
        执行语句并返回数据列
        :rtype:
        """
        log("Select : %s" % sql)
        cursor = self.pymysql.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        return cursor.fetchall()
