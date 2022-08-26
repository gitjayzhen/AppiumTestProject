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

from appium.webdriver.common.mobileby import MobileBy

from framework.core.appiumapi.AppiumBaseApi import AppiumDriver
from framework.initdriver.InitAppiumDriver import InitDriverOption


class TestAppiumBaseApi(unittest.TestCase):

    def setUp(self):
        self.driver = InitDriverOption().get_android_driver()
        self.appium_instances = AppiumDriver(self.driver)

    def tearDown(self):
        self.driver.quit()

    # @unittest.skip("skip 'test_is_displayed' func")
    def test_is_displayed(self):
        print(self.appium_instances.is_displayed(MobileBy.ID, "com.youku.phone:id/img_user"))

    @unittest.skip("skip 'test_find_element_by_want' func")
    def test_find_element_by_want(self):
        print(self.appium_instances.find_element_by_want(MobileBy.ID, "com.youku.phone:id/img_user", 5))

    def test_get_current_activity(self):
        print(self.appium_instances.get_current_activity())


if __name__ == '__main__':
    unittest.main()
