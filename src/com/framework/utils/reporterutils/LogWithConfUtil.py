#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import inspect
import logging
import logging.config


class LoggingController(object):

    def __init__(self):
        pro_root = os.getcwd().split("src")[0]
        f_path = os.path.join(pro_root, "testconfig\\logging.conf")
        logging.config.fileConfig(f_path)    # 采用配置文件
        # create logger  debug,info,warning,error
        self.D = logging.getLogger("debug")
        self.I = logging.getLogger("info")
        self.W = logging.getLogger("warning")
        self.E = logging.getLogger("error")

    def getLogMessage(self, message):
        frame, filename, lineNo, functionName, code, unknowField = inspect.stack()[2]
        '''日志格式：[时间] [类型] [记录代码] 信息'''
        return "[%s- %s -%s] %s" % (filename, lineNo, functionName, message)

    def debug(self, mag):
        mag = self.getLogMessage(mag)
        print self.D.handlers
        self.D.debug(mag)

    def info(self, mag):
        mag = self.getLogMessage(mag)
        print self.I.handlers
        self.I.info(mag)

    def warn(self, mag):
        mag = self.getLogMessage(mag)
        print self.W.handlers
        self.W.warning(mag)

    def error(self, mag):
        mag = self.getLogMessage(mag)
        print self.E.handlers
        self.E.error(mag)

