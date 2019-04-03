import threading
import time

from app.constant.constant import constant


def log(message: str):
    """
    日志打印,可根据 constant静态变量指定
    :param message:
    :return:
    """
    if constant.is_log:
        log_base(message)


def log_base(message: str):
    """
    日志打印基础
    :param message:
    :return:
    """
    print("[" + threading.current_thread().getName() + "] [" + str(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "]: " + str(message))
