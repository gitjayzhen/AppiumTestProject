#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@version: python2.7
@author: ‘jayzhen‘
@license: Apache Licence 
@contact: 2431236868@qq.com
@site: http://www.jayzhen.com
@software: PyCharm
@file: appiumbaseapi.py
@time: 2017/3/28  23:32
"""
from appium.webdriver.common.touch_action import TouchAction
from com.framework.core.adb.commond import AdbCmder
from xml.etree import ElementTree as ET
from com.framework.base.getallpathctl import GetAllPathController
from com.framework.utils.reporterutils.loggingctl import LoggingController
import os
import re

PATH = lambda a: os.path.abspath(a)


class AppiumDriver(object):

    def __init__(self, driver):
        self.android = AdbCmder()
        self.log4py = LoggingController()
        self.driver = driver
        self.taction = TouchAction(self.driver)
        self.path_get = GetAllPathController()
        self.actions = []
        self.xml_file_path = self.path_get.get_dumpxml_path()
        self.pattern = re.compile(r"\d+")

    def __element(self, attrib, name):
        """
        同属性单个元素，返回单个坐标元组，(x, y)
        :args:
        - attrib - node节点中某个属性
        - name - node节点中某个属性对应的值
        """
        Xpoint = None
        Ypoint = None

        if not self.android.get_ui_dump_xml(self.xml_file_path):
            return None
        tree = ET.ElementTree(file=PATH("%s/uidump.xml" % self.xml_file_path))
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if elem.attrib[attrib] == name:
                #获取元素所占区域坐标[x, y][x, y]
                bounds = elem.attrib["bounds"]

                #通过正则获取坐标列表
                coord = self.pattern.findall(bounds)

                #求取元素区域中心点坐标
                Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                break

        if Xpoint is None or Ypoint is None:
            raise Exception("Not found this element(%s) in current activity"%name)

        return (Xpoint, Ypoint)

    def __elements(self, attrib, name):
        """
        同属性多个元素，返回坐标元组列表，[(x1, y1), (x2, y2)]
        """
        pointList = []
        self.android.get_ui_dump_xml(self.xml_file_path)
        tree = ET.ElementTree(file=PATH("%s/uidump.xml" % self.xml_file_path))
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if elem.attrib[attrib] == name:
                bounds = elem.attrib["bounds"]
                coord = self.pattern.findall(bounds)
                Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])

                #将匹配的元素区域的中心点添加进pointList中
                pointList.append((Xpoint, Ypoint))

        return pointList

    def __bound(self, attrib, name):
        """
        同属性单个元素，返回单个坐标区域元组,(x1, y1, x2, y2)
        """
        coord = []

        self.android.get_ui_dump_xml(self.xml_file_path)
        tree = ET.ElementTree(file=PATH("%s/uidump.xml" % self.xml_file_path))
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if elem.attrib[attrib] == name:
                bounds = elem.attrib["bounds"]
                coord = self.pattern.findall(bounds)

        if not coord:
            raise Exception("Not found this element(%s) in current activity"%name)

        return (int(coord[0]), int(coord[1]), int(coord[2]), int(coord[3]))

    def __bounds(self, attrib, name):
        """
        同属性多个元素，返回坐标区域列表，[(x1, y1, x2, y2), (x3, y3, x4, y4)]
        """
        pointList = []
        self.android.get_ui_dump_xml(self.xml_file_path)
        tree = ET.ElementTree(file=PATH("%s/uidump.xml" % self.xml_file_path))
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if elem.attrib[attrib] == name:
                bounds = elem.attrib["bounds"]
                coord = self.pattern.findall(bounds)
                pointList.append((int(coord[0]), int(coord[1]), int(coord[2]), int(coord[3])))

        return pointList

    def __checked(self, attrib, name):
        """
        返回布尔值列表
        """
        boolList = []
        self.android.get_ui_dump_xml(self.xml_file_path)
        tree = ET.ElementTree(file=PATH("%s/uidump.xml" % self.xml_file_path))
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if elem.attrib[attrib] == name:
                checked = elem.attrib["checked"]
                if checked == "true":
                    boolList.append(True)
                else:
                    boolList.append(False)

        return boolList

    def find_element_By_Name(self, name):
        """
        通过元素名称定位单个元素
        usage: findElementByName(u"设置")
        """
        return self.__element("text", name)

    def find_elements_By_Name(self, name):
        """
        通过元素名称定位多个相同text的元素
        """
        return self.__elements("text", name)

    def find_element_By_Class(self, className):
        """
        通过元素类名定位单个元素
        usage: findElementByClass("android.widget.TextView")
        """
        return self.__element("class", className)

    def find_elements_By_Class(self, className):
        """
        通过元素类名定位多个相同class的元素
        """
        return self.__elements("class", className)

    def find_element_By_Id(self, id):
        """
        通过元素的resource-id定位单个元素
        usage: findElementsById("com.android.deskclock:id/imageview")
        """
        return self.__element("resource-id", id)

    def find_elements_By_Id(self, id):
        """
        通过元素的resource-id定位多个相同id的元素
        """
        return self.__elements("resource-id", id)

    def find_element_By_Content_Desc(self, contentDesc):
        """
        通过元素的content-desc定位单个元素
        """
        return self.__element("content-desc", contentDesc)

    def find_elements_By_Content_Desc(self, contentDesc):
        """
        通过元素的content-desc定位多个相同的元素
        """
        return self.__elements("content-desc", contentDesc)

    def get_element_bound_By_Name(self, name):
        """
        通过元素名称获取单个元素的区域
        """
        return self.__bound("text", name)

    def get_element_bounds_By_Name(self, name):
        """
        通过元素名称获取多个相同text元素的区域
        """
        return self.__bounds("text", name)

    def get_element_bound_By_Class(self, className):
        """
        通过元素类名获取单个元素的区域
        """
        return self.__bound("class", className)

    def get_element_bounds_By_Class(self, className):
        """
        通过元素类名获取多个相同class元素的区域
        """
        return self.__bounds("class", className)

    def get_element_bound_By_Content_Desc(self, contentDesc):
        """
        通过元素content-desc获取单个元素的区域
        """
        return self.__bound("content-desc", contentDesc)

    def get_element_bounds_By_Content_Desc(self, contentDesc):
        """
        通过元素content-desc获取多个相同元素的区域
        """
        return self.__bounds("content-desc", contentDesc)

    def get_element_bound_By_Id(self, id):
        """
        通过元素id获取单个元素的区域
        """
        return self.__bound("resource-id", id)

    def get_element_bounds_By_Id(self, id):
        """
        通过元素id获取多个相同resource-id元素的区域
        """
        return self.__bounds("resource-id", id)

    def is_elements_checked_By_Name(self, name):
        """
        通过元素名称判断checked的布尔值，返回布尔值列表
        """
        return self.__checked("text", name)

    def is_elements_checked_By_Id(self, id):
        """
        通过元素id判断checked的布尔值，返回布尔值列表
        """
        return self.__checked("resource-id", id)

    def is_elements_checked_By_Class(self, className):
        """
        通过元素类名判断checked的布尔值，返回布尔值列表
        """
        return self.__checked("class", className)


    # 获取屏幕的尺寸
    def get_screen_size(self, driver):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return (x, y)

    # 操作屏幕向上滑动
    def do_swipe_up(self, driver, duration_time):
        size_screen = self.get_screen_size(driver)
        x_start = int(size_screen[0] * 0.5)
        x_end = x_start
        y_start = int(size_screen[1] * 0.75)
        y_end = int(size_screen[0] * 0.25)
        self.driver.swipe(x_start, y_start, x_end, y_end, duration_time)
        print "log:action swipe up:(%d,%d)-(%d,%d)" % (x_start, y_start, x_end, y_end)

    # 操作屏幕向下滑动
    def do_swipe_down(self, driver, duration_time):
        size_screen = self.get_screen_size(driver)
        x_start = int(size_screen[0] * 0.5)
        x_end = x_start
        y_start = int(size_screen[1] * 0.25)
        y_end = int(size_screen[0] * 0.75)
        self.driver.swipe(x_start, y_start, x_end, y_end, duration_time)
        print "log:action swipe down:(%d,%d)-(%d,%d)" % (x_start, y_start, x_end, y_end)

    # 操作屏幕向左←滑动
    def do_swipe_left(self, driver, duration_time):
        size_screen = self.get_screen_size(driver)
        y_start = int(size_screen[0] * 0.5)
        y_end = y_start
        x_start = int(size_screen[1] * 0.75)
        x_end = int(size_screen[0] * 0.25)
        self.driver.swipe(x_start, y_start, x_end, y_end, duration_time)
        print "log:action swipe left:(%d,%d)-(%d,%d)" % (x_start, y_start, x_end, y_end)

    # 操作屏幕向右→滑动
    def do_swipe_right(self, driver, duration_time):
        size_screen = self.get_screen_size(driver)
        y_start = int(size_screen[0] * 0.5)
        y_end = y_start
        x_start = int(size_screen[1] * 0.25)
        x_end = int(size_screen[0] * 0.75)
        self.driver.swipe(x_start, y_start, x_end, y_end, duration_time)
        print "log:action swipe right:(%d,%d)-(%d,%d)" % (x_start, y_start, x_end, y_end)


    def do_tap_element(self, elemnt):
        """Perform a tap action on the element
        :Args:
         - element - the element to tap
         - x - (optional) x coordinate to tap, relative to the top left corner of the element.
         - y - (optional) y coordinate. If y is used, x must also be set, and vice versa
        :Usage:
        """
        self.taction.tap(elemnt, 10, 10).perform()
        self.log4py.info("appium driver do touch action at element:%s" % (str(elemnt)))


    def do_press(self, el=None, x=None, y=None):
        """Begin a chain with a press down action at a particular element or point
        """
        return self


    def do_long_press(self, el=None, x=None, y=None, duration=1000):
        """Begin a chain with a press down that lasts `duration` milliseconds
        """
        return self


    def do_wait(self, ms=0):
        """Pause for `ms` milliseconds.
        """
        return self


    def do_move_to(self, el=None, x=None, y=None):
        """Move the pointer from the previous point to the element or point specified
        """
        return self


    def do_release(self):
        """End the action by lifting the pointer off the screen
        """
        return self


    def do_perform(self):
        """Perform the action by sending the commands to the server to be operated upon
        """
        # get rid of actions so the object can be reused
        return self


    def do_pinch(self,el):
        '''
        Places two fingers at the edges of the screen and brings them together. 在 0% 到 100% 内双指缩放屏幕，
        '''
        self.driver.pinch(element=el)


    def do_zoom(self, el):
        '''
        放大屏幕 在 100% 以上放大屏幕
        '''
        self.driver.zoom(element=el)


    def do_shake(self):
        '''
        模拟设备摇晃
        '''
        self.driver.shake()

        # convenience method added to Appium (NOT Selenium 3)


    def do_scroll(self, origin_el, destination_el):
        """Scrolls from one element to another
        :Args:
         - originalEl - the element from which to being scrolling
         - destinationEl - the element to scroll to
        :Usage:
            appium_driver.scroll(el1, el2)
        """
        return self

        # convenience method added to Appium (NOT Selenium 3)


    def do_drag_and_drop(self, origin_el, destination_el):
        """Drag the origin element to the destination element
        :Args:
         - originEl - the element to drag
         - destinationEl - the element to drag to
        """
        return self

        # convenience method added to Appium (NOT Selenium 3)


    def do_flick(self, start_x, start_y, end_x, end_y):
        """Flick from one point to another point.
        :Args:
         - start_x - x-coordinate at which to start
         - start_y - y-coordinate at which to start
         - end_x - x-coordinate at which to stop
         - end_y - y-coordinate at which to stop
        :Usage:
            appium_driver.flick(100, 100, 100, 400)
        """
        return self
