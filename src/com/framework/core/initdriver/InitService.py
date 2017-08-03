#!/usr/bin/env python
# -*-coding=utf8 -*-
"""
@version: v1.0
@author: jayzhen
@license: Apache Licence
@contact: jayzhen_testing@163.com
@site: http://blog.csdn.net/u013948858
@software: PyCharm
@time: 2017/5/13  
"""
import subprocess
import os
import string
import time
from com.framework.utils.reporterutils.LoggingUtil import LoggingController
from com.framework.base.GetAllPathCtrl import GetAllPathController
from com.framework.utils.fileutils.CreateConfigUtil import CreateConfigFile


class ServicePort(object):
    def __init__(self):
        self.log4py = LoggingController()
        path_obj = GetAllPathController()
        self.appium_log_path = path_obj.get_appium_logs_path()
        self.appium_port_list = None
        self.device_list = []
        self.cfg = CreateConfigFile()

    def is_port_used(self, port_num):
        """
        检查端口是否被占用
        netstat -aon | findstr port 能够获得到内容证明端口被占用
        :param port_num: 
        :return: 
        """
        flag = False
        try:
            port_res = subprocess.Popen('netstat -ano | findstr %s | findstr LISTENING' % port_num, shell=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE).stdout.readlines()
            reg = re.compile(str(port_num))
            for i in range(len(res)):
                ip_port = res[i].strip().split("   ")
                print ip_port
                if re.search(reg, ip_port[1]):
                    flag = True
                    self.log4py.info(str(port_num) + " port has been occupied." + str(port_res))
            if not flag:
                self.log4py.info(str(port_num) + " port unoccupied." + str(port_res))
        except Exception, e:
            self.log4py.error(str(port_num) + " port get occupied status failure: " + str(e))
        return flag

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
        self.device_list = []
        result = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE).stdout.readlines()
        result.reverse()  # 将readlines结果反向排序
        for line in result[1:]:
            """
            List of devices attached
            * daemon not running. starting it now at tcp:5037 *
            * daemon started successfully *
            """
            if "attached" not in line.strip() and "daemon" not in line.strip():
                self.device_list.append(line.split()[0])
            else:
                break
        return self.device_list

    def get_port_list(self, start):
        """
        只用传送一个开始值，就行了
        :param start: 
        :return: 
        """
        if self.device_list is not None:
            device_num = self.device_list
        else:
            device_num = self.get_devices()
        port_list = self.generat_port_list(start, len(device_num))
        return port_list

    def generate_service_command(self):
        """
        generat_port_list (service_port, conn_port, udid)->command
        :return: 
        """
        self.device_list = self.get_devices()
        self.appium_port_list = self.get_port_list(4490)
        bootstrap_port_list = self.get_port_list(2233)

        service_cmd = []
        for i in range(len(self.device_list)):
            # 20170802 命令中如果带有路径尽量使用斜杠，不使用反斜杠（win环境中是单个），如使用记得变成双斜杠
            appium_path = 'start /b node D:/Android/Appium/node_modules/appium/lib/server/main.js -p '
            # 这两个方式都可以在后台启动一个appium的服务
            # "start /b appium -p "
            cmd = "start /b appium -p " + str(self.appium_port_list[i]) + " -a 127.0.0.1" + " -bp " + str(bootstrap_port_list[i]) + " -U " + str(self.device_list[i]) + " >" + str(self.appium_log_path) + str(self.device_list[i]) + ".txt"
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
                print "启动服务的命令：", i
                # 20170802 尽可能使用subprocess代替os.system执行命令，避免一些错误
                sp = subprocess.Popen(i, shell=True)
                sp.wait()
            flag = True
            self.cfg.set_appium_uuid_port(self.device_list, self.appium_port_list)
            # 等待5秒钟，让服务自己启动一下
            time.sleep(5)
        else:
            flag = False

        return flag


    # TODO(jayzhen_testing@163.com) 待完成细节
    def is_live_service(self, port):
        """
        检查这个端口是否存在一个活动的service，就返回这个端口service的pid
        :param port: 这个port来自appiumservice.ini文件
        :return: pid
        """
        res = subprocess.Popen('netstat -ano | findstr %s | findstr LISTENING' % port, shell=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE).stdout.read()
        if res:
            return res.strip().split(" ")[-1]
        # reg = re.compile(str(port))
        # print port
        # for i in range(len(res)):
        #     ip_port = res[i].strip().split("   ")
        #     print ip_port
        #     if re.search(reg, ip_port[1]):
        #         print ip_port
        #         return ip_port[-1].strip()

        return None

    def kill_service_on_pid(self, pid):
        if pid is not None:
            pid = pid.split()[-1]
            os.system("taskkill /F /PID %s" % pid)
            print "PID：%s 关闭端口服务成功" % pid

    """
    20170802
    @auther jayzhen
    @pm 将service_port中启动的service进行关闭
    """
    def stop_all_appium_server(self):
        c = CreateConfigFile()
        server_list = c.get_all_appium_server_port()
        if len(server_list) > 0:
            for i in range(len(server_list)):
                print "准备关闭端口 %s 的服务" % server_list[i]
                pid = self.is_live_service(server_list[i])
                if pid:
                    self.kill_service_on_pid(pid)
