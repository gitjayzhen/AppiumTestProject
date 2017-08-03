#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@version: python2.7
@author: ‘jayzhen‘
@contact: jayzhen_testing@163.com
@site: https://github.com/gitjayzhen
@software: PyCharm Community Edition
@time: 2017/3/29  13:12
"""
import os
import time

PATH = lambda p: os.path.abspath(p)


class LogController(object):

    def __init__(self, logPath, fileName):
        self.path = logPath
        self.fileName = fileName

        if not os.path.isdir(self.path):
            os.makedirs(self.path)

        self.logFile = file(PATH("%s/%s" % (self.path, self.fileName)), "a")

    def info(self, info):

        timestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.logFile.write("INFO : %s %s\n" %(timestamp, str(info)))
        self.logFile.flush()

    def debug(self,debugInfo):

        timestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.logFile.write("DEBUG: %s %s\n" %(timestamp, str(debugInfo)))
        self.logFile.flush()

    def error(self, errorInfo):

        timestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.logFile.write("ERROR: %s %s\n" %(timestamp, str(errorInfo)))
        self.logFile.flush()

    def close(self):
        self.logFile.close()
