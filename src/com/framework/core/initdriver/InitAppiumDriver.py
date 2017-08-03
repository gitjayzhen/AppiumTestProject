#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@version: v1.0
@author: jayzhen
@license: Apache Licence
@contact: jayzhen_testing@163.com
@site: http://blog.csdn.net/u013948858
@software: PyCharm
@time: 2017/6/3  17:22 当前只能是一个设备
@TODO 多线程并发执行脚本时，需要将端口、手机设备的关联做好;多个设备时desired_capabilities属性只能是一个设备
"""
import re
import os
import subprocess
import time
from appium import webdriver
from com.framework.utils.reporterutils.LoggingUtil import LoggingController
from com.framework.utils.fileutils.ConfigCommonUtil import ConfigController
from com.framework.core.initdriver.InitService import ServicePort
from com.framework.core.initdriver.InitConfig import InitConfiger
from com.framework.core.adb.AdbCommand import AdbCmder


class InitDriverOption(object):
    def __init__(self, sp_obj):
        self.log4py = LoggingController()
        # ServicePort实例化的对象
        self.sp = sp_obj
        self.run_cfg = InitConfiger()
        self.android = AdbCmder()
        self.run_data = None

    def get_desired_capabilities(self, sno):
        device_info = {"udid": sno}
        try:
            result = subprocess.Popen("adb -s %s shell getprop" % sno, shell=True, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE).stdout.readlines()
            for res in result:
                # 系统版本
                if re.search(r"ro\.build\.version\.release", res):
                    device_info["platformVersion"] = (res.split(': ')[-1].strip())[1:-1]
                # 手机型号
                elif re.search(r"ro\.product\.model", res):
                    device_info["deviceName"] = (res.split(': ')[-1].strip())[1:-1]
        except Exception, e:
            self.log4py.error("Get device info happend ERROR :" + str(e))
            return None
        desired_caps_conf = self.run_cfg.get_desired_caps_conf()
        desired_caps = device_info.copy()
        desired_caps.update(desired_caps_conf)
        return desired_caps

    def get_appium_port(self, sno):
        path = (os.getcwd()).split('src')[0] + "\\testconfig\\appiumService.ini"
        ff = ConfigController(path)
        port = ff.get(sno, sno)
        if port:
            print "服务已经启动"
        return port

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
                print "进行卸载操作"
            if self.android.do_install_app(self.run_data["apk_file_path"], self.run_data["pkg_name"]):
                print "需要进行最开始的初始化事件"
        elif int(self.run_data["is_first"]) == 1:
            print "直接进行用例任务"

    def get_android_driver(self, sno):
        desired_caps = self.get_desired_capabilities(sno)
        self.before_create_driver(desired_caps['udid'])
        port = self.get_appium_port(desired_caps["udid"])
        print "port :" + port
        if not port or port is None:
            return None
        while not self.sp.is_port_used(port):
            url = 'http://127.0.0.1:%s/wd/hub' % (port.strip())
            print url
            driver = webdriver.Remote(url, desired_caps)
            if self.run_data["wait_activity"] is not None:
                driver.wait_activity(self.run_data["wait_activity"], 10)
            else:
                driver.implicitly_wait(10)
            return driver
        return None


# TODO(jayzhen_testing@163.com) 解决一下端口服务问题
if __name__ == "__main__":
    sp = ServicePort()
    if sp.start_services():
        ido = InitDriverOption(sp)
        adb = AdbCmder()
        d = adb.get_device_list()
        driver = ido.get_android_driver(d[0])

        driver.close_app()
    sp.stop_all_appium_server()




