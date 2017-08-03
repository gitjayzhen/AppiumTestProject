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
import unittest
from com.framework.core.adb.AdbCommand import AdbCmder


class TestAdbCommand(unittest.TestCase):

    def setUp(self):
        self.cmd = AdbCmder()

    @unittest.skip("demonstrating skipping")
    def test_get_crash_log(self):
        self.cmd.get_crash_log()

    @unittest.skip("demonstrating skipping")
    def test_do_capture_window(self):
        self.cmd.do_capture_window()

    def test_get_ui_dump_xml(self):
        self.cmd.get_ui_dump_xml("W:\\OneDrive\\icloud\\AppiumTestProject\\testresult\\dumpxml")


if __name__ == '__main__':
    unittest.main()
