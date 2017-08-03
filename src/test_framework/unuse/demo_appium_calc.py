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
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '5.1.1'
desired_caps['deviceName'] = '90d1894b7d62'
desired_caps['appPackage'] = 'com.miui.calculator'
desired_caps['appActivity'] = '.cal.NormalCalculatorActivity'

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

driver.find_element_by_name("1").click()

driver.find_element_by_name("5").click()

driver.find_element_by_name("5").click()

driver.find_element_by_name("+").click()

driver.find_element_by_name("6").click()

driver.find_element_by_id("com.android.calculator2:id/equal").click()

driver.quit()
