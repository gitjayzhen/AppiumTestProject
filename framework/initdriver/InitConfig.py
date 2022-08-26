#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@version: v1.0
@author: jayzhen
@license: Apache Licence
@contact: jayzhen_testing@163.com
@site: http://blog.csdn.net/u013948858
@software: PyCharm
@license: Apache Licence
@file: InitConfig.py
@time: 2017/7/31 10:49
"""
from framework.utils.fileutils.ConfigCommonUtil import ConfigController
import os


class InitConfiger(object):

    def __init__(self):
        path = (os.getcwd()).split('src')[0] + "\\testconfig\\run.ini"
        self.cf = ConfigController(path)

    def get_run_conf(self):
        section = "run"
        try:
            # 是否是第一次跑，或者是重新跑，为0时会重新安装指定apk，并执行任务；为1时直接启动安装的app进行任务操作
            is_first = self.cf.get(section, "isFirst")
            # app的包名
            pkg_name = self.cf.get(section, "pkgName")
            # 启动app的main activity
            launch_activity = self.cf.get(section, "launchActivity")
            # 自动化启动app时，需要这个等待来做缓冲，避免启动页面挡住操作
            wait_activity = self.cf.get(section, "waitActivity")
            # 到isFirst为0时，就进行安装操作
            apk_file_path = self.cf.get(section, "apkFilePath")
        except Exception as e:
            return None
        return {"is_first": is_first, "pkg_name": pkg_name, "launch_activity": launch_activity, "wait_activity": wait_activity, "apk_file_path": apk_file_path}

    def set_run_conf(self, is_first, pkg_name, launch_activity, wait_activity, apk_file_path):
        flag = False
        section = "run"
        try:
            self.cf.set(section, "isFirst", is_first)
            self.cf.set(section, "pkgName", pkg_name)
            self.cf.set(section, "launchActivity", launch_activity)
            self.cf.set(section, "waitActivity", wait_activity)
            self.cf.get(section, "apkFilePath", apk_file_path)
            flag = True
        except Exception as e:
            return None
        return flag

    def get_desired_caps_conf(self):
        section = "desired_caps"
        # 这些参数都是启动app时需要的，但是在代码读取参数的时候，不一定都读取，因为有些参数不是固定的
        dc = {}
        try:
            dc["automationName"] = self.cf.get(section, "automationName")
            dc["platformName"] = self.cf.get(section, "platformName")
            # dc["app"] = self.cf.get(section, "app")
            dc["appPackage"] = self.cf.get(section, "appPackage")
            dc["appActivity"] = self.cf.get(section, "appActivity")
            dc["noSign"] = self.cf.get(section, "noSign")
            dc["unicodeKeyboard"] = self.cf.get(section, "unicodeKeyboard")
            dc["resetKeyboard"] = self.cf.get(section, "resetKeyboard")
        except Exception as e:
            return None
        return dc

