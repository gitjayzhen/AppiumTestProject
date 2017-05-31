#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: jayzhen
@time: 2017/5/13  
"""
import subprocess
import os
from com.framework.utils.reporterutils.loggingctl import LoggingController
from com.framework.base.getallpathctl import GetAllPathController


class ServicePort(object):
    def __init__(self):
        self.log4py = LoggingController()
        path_obj = GetAllPathController()
        self.appium_log_path = path_obj.get_appium_logs_path()

    def is_port_used(self, port_num):
        """
        检查端口是否被占用
        netstat -aon | findstr port 能够获得到内容证明端口被占用
        :param port_num: 
        :return: 
        """
        flog = True
        try:
            port_res = subprocess.Popen('netstat -ano | findstr %s' % port_num, shell=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE).stdout.readlines()
            if len(port_res) <= 0:
                self.log4py.info(str(port_num) + " port unoccupied.")
                flog = False
            else:
                self.log4py.error(str(port_num) + " port has been occupied.")
        except Exception, e:
            self.log4py.error(str(port_num) + " port get occupied status failure: " + str(e))
        return flog

    def generat_port_list(self, port_start, num):
        """
        根据链接电脑的设备来创建num个端口号（整形） 电脑有0-65535个端口
        :param num: 
        :return: port_list
        """
        new_port_list = []
        while (len(new_port_list) != num):
            if port_start >= 0 and port_start <= 65535:
                if not self.is_port_used(port_start):
                    new_port_list.append(port_start)
                port_start = port_start + 1
        return new_port_list

    def get_devices(self):
        """
        获取链接电脑的设备数
        :return: 
        """
        devices = []
        result = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE).stdout.readlines()
        result.reverse()  # 将readlines结果反向排序
        for line in result[1:]:
            if "attached" not in line.strip():
                devices.append(line.split()[0])
            else:
                break
        return devices

    def get_port_list(self, start):
        """
        只用传送一个开始值，就行了
        :param start: 
        :return: 
        """
        device_num = self.get_devices()
        port_list = self.generat_port_list(start, len(device_num))
        return port_list

    def generate_service_command(self):
        """
        generat_port_list (service_port, conn_port, udid)->command
        :return: 
        """
        appium_port_list = self.get_port_list(4490)
        bootstrap_port_list = self.get_port_list(2233)
        device_list = self.get_devices()
        service_cmd = []
        for i in range(len(device_list)):
            cmd = "appium -p " + str(appium_port_list[i]) + " -bp " + str(bootstrap_port_list[i]) + " -U " + str(
                device_list[i]) + ">" + str(self.appium_log_path) + str(device_list[i]) + ".txt"
            service_cmd.append(cmd)
        return service_cmd

    def start_services(self):
        """
        根据appium端口、链接手机端口、手机serialno表示，创建一个服务器;启动有些延迟
        需要将appium和手机sno放到文件中供初始化driver使用，xml、ini、conf、json文件格式都行
        :param service_port: 
        :param conn_port: 
        :param udid: 
        :return: 
        """
        service_list = self.generate_service_command()
        flag = False
        if len(service_list) > 0:
            for i in service_list:
                subprocess.Popen(i,shell=True)
            flag = True
        else:
            flag = False
        return flag

# if __name__ == "__main__":
#     sp = ServicePort()
#     print sp.start_services()