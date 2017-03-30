#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@version: python2.7
@author: ‘dell‘
@contact: jayzhen_testing@163.com
@site: https://github.com/gitjayzhen
@software: PyCharm Community Edition
@file: getallpathctl.py
@time: 2017/3/29  13:12
"""
from com.framework.utils.fileutils.configcommonctl import ConfigController
from com.framework.utils.fileutils.filecheckandgetpath import FileChecKController
from com.framework.utils.reporterutils.loggingctl import LoggingController


class GetAllPathController():
    def __init__(self):
        self.fkctl = FileChecKController()
        if self.fkctl.is_has_file("allpath.ini"):
            fp = self.fkctl.get_fileabspath()
        self.cfgctl = ConfigController(fp)
        self.log4py = LoggingController()

    def get_dumpxml_path(self):
        self.log4py.info("executive -get_dumpxml_path- function ")
        return self.cfgctl.get("dumpxmlPath","dumpxmlPath")

    def get_htmlreport_path(self):
        self.log4py.info("executive -get_htmlreport_path- function ")
        return self.cfgctl.get("htmlreportPath","htmlreportPath")

    def get_logs_path(self):
        self.log4py.info("executive -get_logs_path- function ")
        return self.cfgctl.get("logsPath","logsPath")

    def get_capture_path(self):
        self.log4py.info("executive -get_capture_path- function ")
        return self.cfgctl.get("capturePath","capturePath")

if __name__ == "__main__":
    gp = GetAllPathController()
    print gp.get_capture_path()