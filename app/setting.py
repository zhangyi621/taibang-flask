# API后台系统配置文件
from app.constant import constant


class DevAPIConfig(object):
    DEBUG = constant.constant.is_debug
    SECRET_KEY = 'api_cms'


