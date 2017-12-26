#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@version: python2.7
@author: ‘dell‘
@contact: jayzhen_testing@163.com
@site: https://github.com/gitjayzhen
@software: PyCharm Community Edition
@file: GetAllPathCtrl.py
@time: 2017/3/29  13:12
"""
from com.framework.utils.fileutils.ConfigCommonUtil import ConfigController
from com.framework.utils.fileutils.FileCheckAndGetPath import FileChecKController
from com.framework.utils.reporterutils.LoggingUtil import LoggingController
import os

PATH = lambda a: os.path.abspath(a)


class GetAllPathController(object):
    def __init__(self):
        self.fkctl = FileChecKController()
        if self.fkctl.is_has_file("allpath.ini"):
            fp = self.fkctl.get_fileabspath()
        self.cfgctl = ConfigController(fp)
        self.log4py = LoggingController()
        self.pro_path = self.fkctl.get_project_path()

    def get_dumpxml_path(self):
        self.log4py.info("executive -get_dumpxml_path- function ")
        path = os.path.join(self.pro_path, self.cfgctl.get("dumpxmlPath", "dumpxmlPath"))
        if PATH(path):
            self.log4py.info("获取 %s"%path)
            return path
        return None

    def get_htmlreport_path(self):
        self.log4py.info("executive -get_htmlreport_path- function ")
        path = os.path.join(self.pro_path, self.cfgctl.get("htmlreportPath", "htmlreportPath"))
        if PATH(path):
            self.log4py.info("获取 %s" % path)
            return path
        return None

    def get_logs_path(self):
        self.log4py.info("executive -get_logs_path- function ")
        path = os.path.join(self.pro_path, self.cfgctl.get("logsPath", "logsPath"))
        if PATH(path):
            if not os.path.exists(path):
                os.makedirs(path)
            self.log4py.info("获取 %s" % path)
            return path
        return None

    def get_capture_path(self):
        self.log4py.info("executive get_logs_path function ")
        path = os.path.join(self.pro_path, self.cfgctl.get("capturePath", "capturePath"))
        if PATH(path):
            self.log4py.info("获取 %s" % path)
            return path
        return None

    def get_appium_logs_path(self):
        self.log4py.info("executive  get_logs_path  function ")
        path = os.path.join(self.pro_path, self.cfgctl.get("appiumlogPath", "appiumlogPath"))
        if PATH(path):
            if not os.path.exists(path):
                os.makedirs(path)
            self.log4py.info("获取到appium服务的日志路径 %s" % path)
            return path.replace("\\", "/")
        return None