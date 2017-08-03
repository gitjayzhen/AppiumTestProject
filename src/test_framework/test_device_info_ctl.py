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
from com.framework.base.DeviceInfoCtrl import DeviceController

class TestDeviceinfo(unittest.TestCase):
    def setUp(self):
        self.dd = DeviceController()

    def tearDown(self):
        pass

    def test_get_devices_as_dict(self):
        print  self.dd.get_infos_as_dict()


if __name__ == "__main__":
    unittest.main()