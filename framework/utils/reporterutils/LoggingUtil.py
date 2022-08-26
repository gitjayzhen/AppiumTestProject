#!/usr/bin/usr python
# -*- coding:utf8 -*-
"""
@version: python2.7
@author: ‘jayzhen‘
@contact: jayzhen_testing@163.com
@site: https://github.com/gitjayzhen
@software: PyCharm Community Edition
@time: 2017/3/29  13:12
该日志类可以把不同级别的日志输出到不同的日志文件中 
"""

import os
import datetime
import logging
import inspect

abspath = os.getcwd()
logfilepath = abspath.split("src")[0] + "testresult\\logs4script\\"
if not os.path.exists(logfilepath):
    os.makedirs(logfilepath)

# 将对应文件实例化成一个FileHandler对象，让不用级别的日志共用该Filehandler，这样做到日志打印到一个文件中
hd = logging.FileHandler(os.path.abspath(os.path.join(logfilepath, "scripts.log")))
handlers = {logging.DEBUG: hd,logging.INFO: hd,logging.WARNING: hd, logging.ERROR: hd}


class LoggingController(object):

    def __init__(self, level=logging.NOTSET):
        self.__loggers = {}
        log_levels = handlers.keys()
        for level in log_levels:
            logger = logging.getLogger(str(level))
            logger.addHandler(handlers[level])
            logger.setLevel(level)
            self.__loggers.update({level: logger})

    def time_now_formate(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')

    def get_log_message(self, level, message):
        frame, filename, lineNo, functionName, code, unknowField = inspect.stack()[2]
        '''日志格式：[时间] [类型] [记录代码] 信息'''
        relative_path = filename.split("AppiumTestProject")[1]
        relative_path = relative_path.replace("/", ".")
        relative_path = relative_path.replace("\\", ".")
        relative_path = relative_path.replace(".", "", 1)
        return "%s %s %s %s - %s" % (self.time_now_formate(), level, relative_path, lineNo, message)

    def info(self, message):
        message = self.get_log_message("INFO", message)
        self.__loggers[logging.INFO].info(message)

    def error(self, message):
        message = self.get_log_message("ERROR", message)
        self.__loggers[logging.ERROR].warning(message)

    def warning(self, message):
        message = self.get_log_message("WARNING", message)
        self.__loggers[logging.WARNING].warning(message)

    def debug(self, message):
        message = self.get_log_message("DEBUG", message)
        self.__loggers[logging.DEBUG].debug(message)

    def critical(self, message):
        message = self.get_log_message("CRITICAL", message)
        self.__loggers[logging.CRITICAL].critical(message)

