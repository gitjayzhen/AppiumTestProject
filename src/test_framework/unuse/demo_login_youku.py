#!/usr/bin/env python
# -*-coding=utf8 -*-
"""
@version: v1.0
@author: jayzhen
@license: Apache Licence
@contact: jayzhen_testing@163.com
@site: http://blog.csdn.net/u013948858
@software: PyCharm
@time: 2017/2/8  17:22
"""

from appium import webdriver
from selenium.common.exceptions import WebDriverException
import time
from UtilDriverApi.device_info import get_desired_capabilities
from UtilDriverApi.app_swipe_util import AppSwipeUtil

desired_caps = get_desired_capabilities()
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

driver.wait_activity("com.youku.phone/com.youku.ui.activity.HomePageActivity", 10)
info = driver.current_activity
print info.encode("utf-8")
swipe_util = AppSwipeUtil(driver)
driver.implicitly_wait(3)
for i in range(8):
    swipe_util.swipe_right(driver, 1000)

driver.close_app()

'''
appium_driver.find_element_by_id("com.youku.phone:id/img_user").click()
appium_driver.implicitly_wait(3)
appium_driver.find_element_by_id("com.youku.phone:id/ucenter_header_nickname").click()
appium_driver.implicitly_wait(3)
appium_driver.find_element_by_id("com.youku.phone:id/passport_login_type").click()
appium_driver.implicitly_wait(3)
appium_driver.find_element_by_id("com.youku.phone:id/passport_username").send_keys("")
appium_driver.implicitly_wait(3)
appium_driver.find_element_by_id("com.youku.phone:id/passport_password").send_keys(".")
appium_driver.implicitly_wait(3)
appium_driver.find_element_by_id("com.youku.phone:id/passport_login").click()
'''
