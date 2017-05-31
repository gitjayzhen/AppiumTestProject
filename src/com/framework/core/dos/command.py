#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
执行window下特定的dos命令:包括并发执行appium脚本后的关闭启动的端口。
"""
import subprocess
from com.framework.utils.reporterutils.loggingctl import LoggingController


class WindowCmder(object):

    def __init__(self):
        self.log4py = LoggingController()

    def exec_cmd(self, cmd_str):
        """
        :param cmd_str: 
        :return: 命令执行的成功与否
        """
        return

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
        return True

    def kill_service_on_name(self, service_name):
        """
        通过进程的名称来终结进程：taskkill -F -im service_name
        :param service_name: 
        :return: 
        """
        return True
