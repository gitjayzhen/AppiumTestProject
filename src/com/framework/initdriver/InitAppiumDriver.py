#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@version: v1.0
@author: jayzhen
@license: Apache Licence
@contact: jayzhen_testing@163.com
@site: http://blog.csdn.net/u013948858
@software: PyCharm
@time: 2017/8/3  17:22 当前只能是一个设备
@TODO 多线程并发执行脚本时，需要将端口、手机设备的关联做好;多个设备时desired_capabilities属性只能是一个设备
"""
import os
import re
import time
import subprocess
import urllib2

from appium import webdriver
from com.framework.initdriver.InitConfig import InitConfiger

from com.framework.core.adb.AdbCommand import AdbCmder
from com.framework.utils.fileutils.ConfigCommonUtil import ConfigController
from com.framework.utils.reporterutils.LoggingUtil import LoggingController


class InitDriverOption(object):
    def __init__(self):
        self.log4py = LoggingController()
        self.run_cfg = InitConfiger()
        self.android = AdbCmder()
        self.run_data = None

    def get_desired_capabilities(self, sno):
        device_info = {"udid": sno}
        try:
            result = subprocess.Popen("adb -s %s shell getprop" % sno, shell=True, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE).stdout.readlines()
            for res in result:
                if re.search(r"ro\.build\.version\.release", res):
                    device_info["platformVersion"] = (res.split(': ')[-1].strip())[1:-1]
                elif re.search(r"ro\.product\.model", res):
                    device_info["deviceName"] = (res.split(': ')[-1].strip())[1:-1]
                if "platformVersion" in device_info.keys() and "deviceName" in device_info.keys():
                    break
        except Exception, e:
            self.log4py.error("获取手机信息时出错 :" + str(e))
            return None
        desired_caps_conf = self.run_cfg.get_desired_caps_conf()
        desired_caps = device_info.copy()
        desired_caps.update(desired_caps_conf)
        return desired_caps

    def get_appium_port(self, sno):
        """
        这里读取启动服务时生成的那个ini配置文件，读取其中sno对应的状态及服务的port
        :param sno:
        :return:
        """
        path = (os.getcwd()).split('src')[0] + "\\testconfig\\appiumService.ini"
        ff = ConfigController(path)
        try:
            port = ff.get(sno, sno)
            if port:
                self.log4py.info("获取到{}设备对应的appium服务端口{}".format(sno, port))
            return port
        except Exception as e:
            self.log4py.debug("{}设备对应的appium未启动".format(sno))
            return None

    def is_port_used(self, port_num):
        """
        检查端口是否被占用
        netstat -aon | findstr port 能够获得到内容证明端口被占用
        """
        flag = False
        try:
            port_res = subprocess.Popen('netstat -ano | findstr %s | findstr LISTENING' % port_num, shell=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE).stdout.readlines()
            reg = re.compile(str(port_num))
            for i in range(len(port_res)):
                ip_port = port_res[i].strip().split("   ")
                if re.search(reg, ip_port[1]):
                    flag = True
                    self.log4py.info(str(port_num) + " 端口的服务已经启动." )
            if not flag:
                self.log4py.info(str(port_num) + " 端口的服务未启动.")
        except Exception, e:
            self.log4py.error(str(port_num) + " port get occupied status failure: " + str(e))
        return flag

    def before_create_driver(self, sno):
        """
        在实例appium driver前，进行设备的操作：安装、卸载
        :param sno:
        :return:
        """
        self.android.set_serialno_num(sno)
        self.run_data = self.run_cfg.get_run_conf()
        if int(self.run_data["is_first"]) == 0:
            if self.android.is_install_app(self.run_data["pkg_name"]):
                self.android.do_uninstall_app(self.run_data["pkg_name"])
                self.log4py.info("对测试设备进行卸载应用操作：{}".format(self.run_data["pkg_name"]))
            if self.android.do_install_app(self.run_data["apk_file_path"], self.run_data["pkg_name"]):
                self.log4py.info("重新安装应用成功")
        elif int(self.run_data["is_first"]) == 1:
            self.log4py.info("非首次执行，可以直接进行正常用例操作")

    def get_android_driver(self, sno):
        desired_caps = self.get_desired_capabilities(sno)
        self.before_create_driver(desired_caps['udid'])
        port = self.get_appium_port(desired_caps["udid"])
        if not self.is_port_used(port):
            self.log4py.debug("设备号[{}]对应的appium服务没有启动".format(desired_caps['udid']))
            return None
        url = 'http://127.0.0.1:%s/wd/hub' % (port.strip())
        self.log4py.debug(url)
        self.log4py.debug(desired_caps)
        num = 0
        while num <= 5:
            try:
                driver = webdriver.Remote(url, desired_caps)
            except urllib2.URLError as e:
                self.log4py.error("连接appium服务，实例化driver时出错，尝试重连...({})".format(num))
                num = num + 1
                continue
            if self.run_data["wait_activity"] is not None:
                driver.wait_activity(self.run_data["wait_activity"], 10)
            else:
                driver.implicitly_wait(10)
            self.log4py.info("webdriver连接信息：{}：{}".format(url, str(desired_caps)))
            return driver
        return None







