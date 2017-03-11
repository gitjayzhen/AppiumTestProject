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

def __get_devices():
    devices = []
    result = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
    result.reverse()  #将readlines结果反向排序
    for line in result[1:]:
        if "attached" not in line.strip():
            devices.append(line.split()[0])
        else:
            break
    return devices

def __get_info(sno):
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
        return sno,phone_brand,phone_model,os_version,ip
    except Exception,e:
        print ">>> Get device info happend ERROR :"+ str(e)
        return None

def get_device_infos_as_dict():
    try:
        info = {}
        lists = __get_devices()
        if not lists or len(lists) <= 0:
            print ">>>NO Device connected"
            return None
        for sno in lists:
            sno,phone_brand,phone_model,os_version,ip = __get_info(sno)
            info[sno] = {"phone_brand":phone_brand,"phone_model":phone_model,"os_version":os_version,"ip":ip}
        return info
    except TypeError,e:
        print "func get_device_infos_as_dict happend ERROR!!!"
        return None

def get_desired_capabilities():
    info = get_device_infos_as_dict()
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['appPackage'] = 'com.youku.phone'
    desired_caps['appActivity'] = '.ActivityWelcome'
    for i in info:
        desired_caps['platformVersion'] = info[i]["os_version"]
        desired_caps['deviceName'] = i
    return desired_caps

def get_android_driver():
    # kill_package_process("com.youku.phone")
    desired_caps = get_desired_capabilities()
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    return driver

def kill_package_process(package_name):
    subprocess.Popen("adb shell am force-stop %s"%package_name,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE).wait()







