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
from xml.etree import ElementTree as ET
import os


PATH = lambda a: os.path.abspath(a)


class XMLNodeChecker(object):

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