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
import re
import os
import threading
from multiprocessing import Process
import string
import time
from com.framework.utils.reporterutils.LoggingUtil import LoggingController
from com.framework.base.GetAllPathCtrl import GetAllPathController
from com.framework.utils.fileutils.CreateConfigUtil import CreateConfigFile


class RunServer(threading.Thread):
    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd

    def run(self):
        # 20170802 尽可能使用subprocess代替os.system执行命令，避免一些错误
        # os.system(i)
        # fp = open("AppiumTestProject/testresult/logs4appium/933733961f382.txt", 'a')
        # 20171219 可以使用fp对象传给stdout
        p = subprocess.Popen(self.cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        p.wait()
        time.sleep(5)


class ServicePort(object):
    def __init__(self):
        self.log4py = LoggingController()
        path_obj = GetAllPathController()
        self.appium_log_path = path_obj.get_appium_logs_path()
        self.appium_port_list = []
        self.bootstrap_port_list = []
        self.device_list = []
        self.cfg = CreateConfigFile()
        self.tmp = {}

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
                    self.log4py.info(str(port_num) + " 端口已经在使用,对应的进程是：" + str(ip_port[-1]))
                    self.tmp[port_num] = ip_port[-1]
            if not flag:
                self.log4py.info(str(port_num) + " 端口没有被占用.")
        except Exception, e:
            self.log4py.error(str(port_num) + " port get occupied status failure: " + str(e))
        return flag

    def is_live_service(self, port):
        """
        检查这个端口是否存在一个活动的service，就返回这个端口service的pid
        :param port: 这个port来自appiumservice.ini文件
        """
        return self.is_port_used(port)

    def __generat_port_list(self, port_start, num):
        """
        根据链接电脑的设备来创建num个端口号（整形） 电脑有0-65535个端口
        """
        new_port_list = []
        while len(new_port_list) != num:
            if port_start >= 0 and port_start <= 65535:
                if not self.is_port_used(port_start):
                    new_port_list.append(port_start)
                port_start = port_start + 1
        return new_port_list

    def __get_devices(self):
        """
        获取链接电脑的设备数
        """
        self.device_list = []
        try:
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
        except Exception, e:
            self.log4py.error("启动appium前查询连接的设备情况，发生错误：{}".format(str(e)))
        return self.device_list

    def __get_port_list(self, start):
        """
        只用传送一个开始值，就行了
        """
        if self.device_list is not None:
            device_num = self.device_list
        else:
            device_num = self.__get_devices()
        port_list = self.__generat_port_list(start, len(device_num))
        return port_list

    def __generate_service_command(self):
        """
        generat_port_list (service_port, conn_port, udid)->command
        :return 是一个以端口号为key的dict
        """
        self.appium_port_list = self.__get_port_list(4490)
        self.bootstrap_port_list = self.__get_port_list(2233)
        # 20170804 将service_cmd list类型换成dict --> {port:cmd,port1:cmd2} ,port留作执行cmd后的端口校验
        service_cmd = {}
        for i in range(len(self.device_list)):
            # 20170802 命令中如果带有路径尽量使用斜杠，不使用反斜杠（win环境中是单个），如使用记得变成双斜杠
            # appium_path = 'start /b node D:/Android/Appium/node_modules/appium/lib/server/main.js -p '
            # 这两个方式都可以在后台启动一个appium的服务
            cmd = "start /b appium -p " + str(self.appium_port_list[i]) + " -a 127.0.0.1" + " -bp " + str(self.bootstrap_port_list[i]) + " -U " + str(self.device_list[i]) + " >" + str(self.appium_log_path) + str(self.device_list[i]) + ".txt"
            service_cmd[str(self.appium_port_list[i])] = cmd
        return service_cmd

    def kill_service_on_pid(self, pid):
        if pid is not None:
            os.system("taskkill -F -PID %s" % pid)
            self.log4py.info("PID：%s 关闭端口服务成功" % pid)

    def stop_all_appium_server(self):
        """
        20170802
        @auther jayzhen
        @pm 将service_port中启动的service进行关闭
        """
        c = CreateConfigFile()
        server_list = c.get_all_appium_server_port()
        if len(server_list) <= 0:
            self.log4py.debug("请你确认是否有appium服务启动")
            return None

        for i in range(len(server_list)):
            self.log4py.info("准备关闭端口 %s 的服务" % server_list[i])
            if self.is_live_service(server_list[i]):
                self.kill_service_on_pid(self.tmp[server_list[i]])

    def check_service(self, times=5):
        # 检查服务是否已经启动
        begin = time.time()
        for i in range(len(self.appium_port_list)):
            p = self.appium_port_list[i]
            while time.time() - begin <= times:
                if self.is_live_service(p):
                    self.log4py.info("appium server 端口为{}的服务已经启动,bootstrap监听的端口也已设置好".format(p))
                    # 服务启动正常，就写入配置文件
                    self.cfg.set_appium_uuid_port(self.device_list[i], self.appium_port_list[i], self.bootstrap_port_list[i])
                    break
                self.log4py.info("appium server 端口为{}的服务未启动".format(p))

    def start_services(self):
        """
        根据appium端口、链接手机端口、手机serialno表示，创建一个服务器;启动有些延迟
        需要将appium和手机sno放到文件中供初始化driver使用，xml、ini、conf、json文件格式都行
        20171218 现在考虑一个问题：是否在没有设备连接的时候就把这个服务启动起来？
        如果启动了：写入配置的内容如何定义？后续有设备连接上了，如果刷新配置文件中的内容？
        最终还是没有设备就不启动了（或者给个开关也行）
        """
        self.device_list = self.__get_devices()
        if self.device_list is None or len(self.device_list) <= 0:
            self.log4py.debug("当前没有设备连接到pc，无法进行appium服务端口的映射，无法启动对应的服务")
            return None

        service_list = self.__generate_service_command()
        # 启动服务
        if len(service_list) > 0:
            for i in service_list:
                self.log4py.info("通过线程启动服务的命令：{}".format(service_list[i]))
                t1 = RunServer(service_list[i])
                p = Process(target=t1.start())
                p.start()
                # 20171221 等待5秒钟，等待一下进程
                time.sleep(5)
