#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: jayzhen
@time: 2017/2/8  17:22
"""
import re
import time
import subprocess
from appium import webdriver
from com.framework.utils.reporterutils.loggingctl import LoggingController


class InitDriverOption(object):
    def __init__(self):
        self.log4py = LoggingController()

    def __get_devices(self):
        devices = []
        result = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
        # 将readlines结果反向排序
        result.reverse()
        for line in result[1:]:
            if "attached" not in line.strip():
                devices.append(line.split()[0])
            else:
                break
        return devices

    def __get_info(self, sno):
        phone_brand = None
        phone_model = None
        os_version = None
        dpi = None
        image_resolution = None
        ip = None
        try:
            result = subprocess.Popen("adb -s %s shell getprop"%sno, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
            for res in result:
                #系统版本
                if re.search(r"ro\.build\.version\.release",res):
                    os_version = (res.split(': ')[-1].strip())[1:-1]
                #手机型号
                elif re.search(r"ro\.product\.model",res):
                    phone_model = (res.split(': ')[-1].strip())[1:-1]
                #手机品牌
                elif re.search(r"ro\.product\.brand",res):
                    phone_brand = (res.split(': ')[-1].strip())[1:-1]
                #手机IP
                elif re.search(r'dhcp\.wlan0\.ipaddress', res):
                    ip = (res.split(': ')[-1].strip())[1:-1]
            return sno, phone_brand, phone_model, os_version, ip
        except Exception,e:
            self.log4py.error("Get device info happend ERROR :" + str(e))
            return None

    def get_device_infos_as_dict(self):
        try:
            info = {}
            lists = self.__get_devices()
            if not lists or len(lists) <= 0:
                self.log4py.info("NO Device connected")
                return None
            for sno in lists:
                sno, phone_brand, phone_model, os_version, ip = self.__get_info(sno)
                info[sno] = {"phone_brand": phone_brand, "phone_model": phone_model, "os_version":os_version,"ip":ip}
            return info
        except TypeError, e:
            self.log4py.error("func get_device_infos_as_dict happend ERROR!!!")
            return None

    def get_desired_capabilities(self):
        info = self.get_device_infos_as_dict()
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        #desired_caps['noSign'] = 'ture'
        #支持中文
        desired_caps['unicodeKeyboard'] = 'True'
        desired_caps['resetKeyboard'] = 'True'
        desired_caps['appPackage'] = 'com.youku.phone'
        desired_caps['appActivity'] = '.ActivityWelcome'
        for i in info:
            desired_caps['platformVersion'] = info[i]["os_version"]
            desired_caps['deviceName'] = i
            desired_caps['udid'] = i
        return desired_caps

    def get_android_driver(self):
        desired_caps = self.get_desired_capabilities()
        driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        driver.wait_activity("com.youku.phone/com.youku.ui.activity.HomePageActivity", 10)
        return driver








