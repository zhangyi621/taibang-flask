import argparse

from flask_cors import CORS

from app import create_api_app
# 读取启动时的额外参数
from app.constant import constant
import json
import os

parser = argparse.ArgumentParser()

# 启动时可添加额外命令参数 -threading -debug
parser.add_argument("-threading", action="store_true", help="开启多线程")
parser.add_argument("-log", action="store_true", help="开启日志打印")
parser.add_argument("-debug", action="store_true", help="开启调试模式，不修改标记与不新增记录")
parser.add_argument("-config", nargs=1, type=str, help="指定配置文件")
parser.add_argument("-port", nargs=1, type=int, help="指定端口号", default=[91])
# from api_run import parser
# from app.constant import constant

# def run_config():
args = parser.parse_args()

config = "db-test.json" if args.config is None else args.config[0]

# 获取工程路径
constant.constant.project_path = os.path.split(os.path.realpath(__file__))[0]

config_path = constant.constant.project_path + "/" + config

# 打开配置文件
file_content = open(config_path, encoding="utf-8")

# 解析JSON
json_obje = json.load(file_content)

constant.constant.dbconfig = json_obje

constant.constant.is_log = False if args.log is False else True
constant.constant.is_debug = False if args.debug is False else True
constant.constant.threading = args.threading or False

api_app = create_api_app()

# 入口运行文件
# print(api_app.url_map)
api_app.run(host='0.0.0.0', port=args.port[0])
CORS(api_app)  # 允许跨站请求
