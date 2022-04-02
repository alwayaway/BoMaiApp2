# coding:utf-8

"""
Time:     ${DATE} ${TIME}
Author:   alwayaway
e-mail: alwayaway@foxmail.com
Version:  V 1.1
File:     ${NAME}.py
Describe: Config by sqlite3 or  file[.ini/.conf]
"""

import logging
import logging.handlers


class Log:
    def __init__(self, filepath: str, log_name: str = 'log', size: int = 2048000):
        """
        初始化日志模块，检查日志文件大小，超过一定大侠自动更名并删除多余旧日志文件
        对logging 进行简单封装
        :param filepath: 日志路径
        :param log_name: 日志文件名称
        :param size: 日志最大存储 单位:bytes
        """
        self._log = logging.getLogger(log_name)
        self._error = logging.getLogger(f"{log_name}_err")

        self._log.setLevel(logging.INFO)
        self._error.setLevel(logging.DEBUG)

        LOG_FORMAT = "%(asctime)s - %(levelname)-8s : %(message)s"
        DATE_FORMAT = "%m/%d/%Y %H:%M:%S"
        self.formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

        rotatingHandler = logging.handlers.RotatingFileHandler(f'{filepath}/{log_name}.log',
                                                               maxBytes=size, backupCount=2)
        rotatingHandler_err = logging.handlers.RotatingFileHandler(f'{filepath}/{log_name}_err.log',
                                                                   maxBytes=size, backupCount=2)
        rotatingHandler.setFormatter(self.formatter)
        rotatingHandler_err.setFormatter(self.formatter)

        self._log.addHandler(rotatingHandler)
        self._error.addHandler(rotatingHandler_err)

        """对日志级别进行封装，方便调用"""
        self._log_level_dict = {
            'info': self._log.info,
            'debug': self._error.debug,
            'warning': self._log.warning,
            'error': self._error.error,
            'exception': self._error.exception,
            'critical': self._log.critical,
        }

        """对日志选项进行封装，方便调用"""
        self._log_option = {
            'shutdown': logging.shutdown
        }

    def set_console(self, console=None):
        streamHandler = logging.StreamHandler(console)
        streamHandler.setFormatter(self.formatter)
        self._log.addHandler(streamHandler)
        # self._error.addHandler(streamHandler)

    def info(self, *args, **kwargs):
        self._log_level_dict["info"](*args, **kwargs)

    def debug(self, *args, **kwargs):
        self._log_level_dict["debug"](*args, **kwargs)

    def warning(self, *args, **kwargs):
        self._log_level_dict["warning"](*args, **kwargs)

    def error(self, *args, **kwargs):
        self._log_level_dict["error"](*args, **kwargs)

    def exception(self, *args, **kwargs):
        self._log_level_dict["exception"](*args, **kwargs)

    def critical(self, *args, **kwargs):
        self._log_level_dict["critical"](*args, **kwargs)

    def shutdown(self):
        self._log_option["shutdown"]()
