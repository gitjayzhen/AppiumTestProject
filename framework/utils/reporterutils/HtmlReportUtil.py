#!/usr/bin/env python
# -*- coding:UTF-8 -*-
"""
@version: python2.7
@author: ‘jayzhen‘
@contact: jayzhen_testing@163.com
@site: https://github.com/gitjayzhen
@software: PyCharm Community Edition
@time: 2017/3/29  13:12
"""
import os
from framework.utils.reporterutils.LoggingUtil import LoggingController
from framework.utils.fileutils.ConfigCommonUtil import ConfigController
from framework.utils.fileutils.FileCheckAndGetPath import FileChecKController
from framework.utils.formatutils.DateTimeUtil import DateTimeManager

'''
创建一个html文件，并返回文件的对象
'''
def html_reporter():
    logger = LoggingController()
    fc = FileChecKController()
    pro_path = fc.getProjectPath()
    boolean = fc.is_has_file("framework.ini")
    if boolean:
        inipath = fc.get_fileabspath()
        fw_conf = ConfigController(inipath)
    htmlrp_path = fw_conf.get("htmlreportPath", "htmlreportPath")
    htmreportl_abs_path = os.path.join(pro_path,htmlrp_path)
    timecurrent = DateTimeManager().formatedTime("%Y-%m-%d-%H-%M-%S")
    logger.debug("=====创建了一个html文件报告,路径是：："+htmreportl_abs_path)
    file_path = str(htmreportl_abs_path)+timecurrent+"-LDP-TestingRreporter.html"
    try:
        if os.path.exists(file_path):
            html_obj = open(file_path, "a") #打开文件   追加
            return html_obj
        else:
            html_obj = open(file_path, "wb+")
            return html_obj
    except Exception as e:
        logger.error("创建html_reporter出现错误"+str(e))


