#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@version: python2.7
@author: ‘jayzhen‘
@license: Apache Licence 
@contact: 2431236868@qq.com
@site: http://www.jayzhen.com
@software: PyCharm
@file: test_device_info_ctl.py
@time: 2017/3/26  18:27
"""
import unittest
from com.framework.base.deviceinfoctl import DeviceController

class TestDeviceinfo(unittest.TestCase):
    def setUp(self):
        self.dd = DeviceController()
        self.dl = self.dd.get_devices()
    def tearDown(self):
        pass

    def test_get_devices_as_dict(self):
        print  self.dd.get_devices_as_dict()
    def test_current_package_name(self):
        s = self.dl[0]
        print self.dd.current_package_name(s)
    def test_current_activity(self):
        s = self.dl[0]
        print self.dd.current_activity(s)

if __name__ == "__main__":
    unittest.main()