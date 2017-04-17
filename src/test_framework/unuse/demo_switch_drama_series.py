#!/usr/bin/env python
#-*- coding:utf-8 -*-

from device_info import get_android_driver
import time

driver = get_android_driver()
try:
    time.sleep(10)
    driver.find_element_by_id("com.youku.phone:id/tool_bar_hot_word").click()
    driver.implicitly_wait(3)
    element_a = driver.find_element_by_id("com.youku.phone:id/et_widget_search_text")
    element_a.click()
    element_a.send_keys("三生三世十里桃花")
    driver.implicitly_wait(3)
    driver.find_element_by_id("com.youku.phone:id/tv_right").click()
finally:
    driver.close_app()
