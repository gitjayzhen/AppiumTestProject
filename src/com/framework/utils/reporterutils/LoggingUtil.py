#!/usr/bin/usr python
# -*- coding:utf8 -*-
"""
@version: python2.7
@author: ‘dell‘
@contact: jayzhen_testing@163.com
@site: https://github.com/gitjayzhen
@software: PyCharm Community Edition
@time: 2017/3/29  13:12
该日志类可以把不同级别的日志输出到不同的日志文件中 
"""
import os
import sys
import time
import logging
import inspect

abspath = os.getcwd()
logfilepath = abspath.split("src")[0] + "testresult\\logs4script\\"    # 当前项目的目录
if not os.path.exists(logfilepath):
    os.makedirs(logfilepath)
handlers = {logging.NOTSET: os.path.join(logfilepath, "log-notset.log"),
            logging.DEBUG: os.path.join(logfilepath, "log-debug.log"),
            logging.INFO: os.path.join(logfilepath, "log-info.log"),
            logging.WARNING: os.path.join(logfilepath, "log-warning.log"),
            logging.ERROR: os.path.join(logfilepath, "log-error.log"),
            logging.CRITICAL: os.path.join(logfilepath, "log-critical.log")}


def create_file_handlers():
    logLevels = handlers.keys()
    for level in logLevels:
        path = os.path.abspath(handlers[level])
        handlers[level] = logging.FileHandler(path)

# 加载模块时创建全局变量
create_file_handlers()


class LoggingController():

    def __init__(self, level=logging.NOTSET):
        self.__loggers = {}  # 将每个级别的logger对象存放在dict中
        logLevels = handlers.keys()
        for level in logLevels:
            # 实例化一个logger对象，用getLogger()将永远返回相同Logger对象的引用。
            logger = logging.getLogger(str(level))
            # 如果不指定level，获得的handler似乎是同一个handler?
            logger.addHandler(handlers[level])
            logger.setLevel(level)
            self.__loggers.update({level: logger})

    def time_now_formate(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def get_log_message(self, level, message):
        # 在堆栈中获取当前执行文件或类或方法
        frame, filename, lineNo, functionName, code, unknowField = inspect.stack()[2]
        '''日志格式：[时间] [类型] [记录代码] 信息'''
        return "[%s] [%s] [%s - %s - %s] %s" % (self.time_now_formate(), level, filename, lineNo, functionName, message)

    def info(self, message):
        message = self.get_log_message("info", message)
        self.__loggers[logging.INFO].info(message)

    def error(self, message):
        message = self.get_log_message("error", message)
        self.__loggers[logging.ERROR].error(message)

    def warning(self, message):
        message = self.get_log_message("warning", message)
        self.__loggers[logging.WARNING].warning(message)

    def debug(self, message):
        message = self.get_log_message("debug", message)
        self.__loggers[logging.DEBUG].debug(message)

    def critical(self, message):
        message = self.get_log_message("critical", message)
        self.__loggers[logging.CRITICAL].critical(message)

    def log_close(self):
        logLevels = handlers.keys()
        for level in logLevels:
            handlers[level].close()

