#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@version: python2.7
@author: ‘jayzhen‘
@contact: jayzhen_testing@163.com
@site: https://github.com/gitjayzhen
@software: PyCharm Community Edition
1.该类主要处理appium多机并发测试场景下生成的端口与机器的设备号映射。
a.接受初始化service中接受到device_list和service_list
b.先判断是否存在固定的config文件，如果没有就创建；有，就覆盖模式进行写入
c.循环遍历这个list并写入文件中
"""
import os
import ConfigParser
from com.framework.utils.reporterutils.LoggingUtil import LoggingController


class CreateConfigFile(object):

    def __init__(self):
        self.cfg = ConfigParser.ConfigParser()
        self.log4py = LoggingController()
        self.path = (os.getcwd()).split('src')[0] + "\\testconfig"

    def set_appium_uuids_ports(self, device_list, port_list):
        """
        遍历list,按照下表进行对应映射
        :param device_lsit: 手机uuid
        :param port_list: pc启动的appium服务端口
        """
        f_path = self.create_config_file(self.path)

        if len(device_list) > 0 and len(port_list) > 0:
            self.cfg.read(f_path)
            for i in range(len(device_list)):
                filed = device_list[i]
                key = filed
                value = port_list[i]
                # 因为是覆盖写入，没有section，需要先添加再设置, 初始化的服务都加一个run的标识
                self.cfg.add_section(filed)
                self.cfg.set(filed, key, value)
                self.cfg.set(filed, "run", "0")
            self.cfg.write(open(f_path, 'wb'))
            self.log4py.debug("设备sno与appium服务端口映射已写入appiumService.ini配置文件:{}--{}".format(key, value))

    def set_appium_uuid_port(self, device, port, bp):
        """
        如果这样一个一个的写入到配置文件中，是追加还是覆盖？如果是覆盖的，服务启动完成后就剩一个配置，所以不行
        如果是追加，需要判断配置文件中是否已经有了相同的section，有就更新，没有就添加
        :param device: 手机uuid
        :param port pc启动的appium服务端口
        """
        f_path = os.path.join(self.path, 'appiumService.ini')
        if not os.path.exists(f_path):
            os.makedirs(f_path)
        if device is not None and port is not None:
            self.cfg.read(f_path)
            sec = device
            key = sec
            value = port
            if sec in self.cfg.sections():
                self.cfg.set(sec, key, value)
                self.cfg.set(sec, "bp", bp)
                self.cfg.set(sec, "run", "0")
            else:
                self.cfg.add_section(sec)
                self.cfg.set(sec, key, value)
                self.cfg.set(sec, "bp", bp)
                self.cfg.set(sec, "run", "0")
            self.cfg.write(open(f_path, 'wb'))
            self.log4py.debug("设备sno与appium服务端口映射已写入appiumService.ini配置文件:{}--{}".format(key, value))

    def create_config_file(self, path):
        """
        如果path这个文件不存在，就创建这个文件;存在就清空文件
        :param path: 
        :return: 
        """
        if not os.path.exists(path):
            os.makedirs(path)
        f_path = os.path.join(path, 'appiumService.ini')
        f = open(f_path, "wb")
        f.close()
        return f_path

    def get_all_appium_server_port(self):
        f_path = os.path.join(self.path, 'appiumService.ini')
        port_list = []
        if os.path.exists(f_path):
            self.cfg.read(f_path)
            section_list = self.cfg.sections()
            for sl in section_list:
                port_list.append(self.cfg.get(sl, sl))
                port_list.append(self.cfg.get(sl, "bp"))
        return port_list

