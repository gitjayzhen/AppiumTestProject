#-*-coding=utf8 -*-
import os
import re
import time
from com.framework.core.adb.AdbCommand import AdbCmder
from com.framework.utils.reporterutils.LoggingUtil import LoggingController

class DeviceController():
    def __init__(self):
        self.android = AdbCmder()
        self.log4py = LoggingController()
    '''
        获取连接上电脑的手机设备，返回一个设备名的list
    '''
    def get_devices(self):
        sno_list = self.android.get_device_list()
        return sno_list

    '''
    根据不同的需求，设计了返回dict和list格式的两个function。
    '''
    def get_infos_as_dict(self):
        try:
            info = {}
            lists = self.get_devices()
            if not lists or len(lists) <= 0:
                self.log4py.info("NO Device connected")
                return None
            for sno in lists:
                sno,phone_brand,phone_model,os_version,ram,dpi,image_resolution,ip = self.get_info(sno)
                info[sno] = {"phone_brand":phone_brand,"phone_model":phone_model,"ram":ram,"os_version":os_version,"dpi":dpi,"image_resolution":image_resolution,"ip":ip}
            return info
        except TypeError,e:
            self.log4py.error(e)
            return None

    def get_infos_as_list(self):
        info_list = self.get_devices_as_dict()
        devices_as_lsit = ["All"]
        for i in info_list:
            a = info_list[i]["phone_brand"]
            b = info_list[i]["phone_model"]
            c = info_list[i]["os_version"]
            d = info_list[i]["dpi"]
            e = info_list[i]["image_resolution"]
            f = info_list[i]["ip"]
            t = a+"  ::  "+b+"  ::  "+c+"  ::  "+d+"  ::  "+e+"  ::  "+f
            devices_as_lsit.append(t)
        return devices_as_lsit

    '''
    通过adb命令来获取连接上电脑的设备的信息。
    '''
    def get_info(self,sno):
        phone_brand = None
        phone_model = None
        os_version = None
        ram = None
        dpi = None
        image_resolution = None
        ip = None
        try:
            result = self.android.shell("cat /system/build.prop").stdout.readlines()
            for res in result:
                #系统版本
                if re.search(r"ro\.build\.version\.release",res):
                    os_version = res.split('=')[-1].strip()
                #手机型号
                elif re.search(r"ro\.product\.model",res):
                    phone_model = res.split('=')[-1].strip()
                #手机品牌
                elif re.search(r"ro\.product\.brand",res):
                    phone_brand = res.split('=')[-1].strip()
            ip = self.android.shell("getprop dhcp.wlan0.ipaddress").stdout.read()
            dpi = self.android.shell("getprop ro.sf.lcd_density").stdout.read()
            proc_meninfo = self.android.shell("cat /proc/meminfo").stdout.readline()
            ram = (int(proc_meninfo.split(" ")[-2])//1000000)
            if int(proc_meninfo.split(" ")[-2])%1000000 >= 500000:
                ram += 1
            res_4_2 = self.android.shell("dumpsys window").stdout.read()
            res_4_4 = self.android.shell("wm size").stdout.read()
            r_4_2 = "init=(\d*x\d*)"
            r_4_4 = "Physical size: (\d*x\d*)"
            reg_4_4 = re.compile(r_4_4)
            reg_4_2 = re.compile(r_4_2)
            image_list_4_4 = re.findall(reg_4_4,res_4_4)
            image_list_4_2 = re.findall(reg_4_2,res_4_2)
            if len(image_list_4_4) > 0:
                image_resolution = image_list_4_4[0]
            elif len(image_list_4_2) > 0:
                image_resolution = image_list_4_2[0]
            else:
                image_resolution = "NULL"
            return sno,phone_brand,phone_model,os_version,str(ram)+"GB",dpi.strip(),image_resolution,ip.strip()
        except Exception,e:
            self.log4py.error("Get device info happend ERROR :"+ str(e))
            return None
