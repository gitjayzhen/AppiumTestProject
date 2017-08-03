#!/usr/bin/env python
# -*-coding=utf8 -*-
"""
@version: v1.0
@author: jayzhen
@license: Apache Licence
@contact: jayzhen_testing@163.com
@site: http://blog.csdn.net/u013948858
@software: PyCharm
"""
"""
执行window下特定的dos命令:包括并发执行appium脚本后的关闭启动的端口。
"""
import subprocess
from com.framework.utils.reporterutils.LoggingUtil import LoggingController


class WindowCmder(object):

    def __init__(self):
        self.log4py = LoggingController()

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

    def exec_cmd(self, cmd_str):
        """
        :param cmd_str: 
        :return: 命令执行的成功与否
        """
        subprocess.Popen(cmd_str, shell=True)
        return True

    def exec_cmd_console(self, cmd_str):
        """
        :param cmd_str: 
        :return: 将命令执行后的结果内容返回
        """
        content = ""
        return content

    def kill_service_on_pid(self, pid):
        """
        杀死为pid进程号的进程:taskkill -F -PID pid_num
        :param pid: 
        :return: 
        """
        return self.exec_cmd("taskkill -F -PID %s" % pid)

    def kill_service_on_name(self, service_name):
        """
        通过进程的名称来终结进程：taskkill -F -im service_name
        :param service_name: 
        :return: 
        """
        return True
