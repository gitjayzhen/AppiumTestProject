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
# 需要安装pychartdir模块
import string
from com.framework.core.adb.AdbCommand import AdbCmder
from pychartdir import *


class AppPerformanceMonitor():
    def  __init__(self,sno,times,pkg_name):
        # 打开待测应用，运行脚本，默认times为30次（可自己手动修改次数），获取该应用cpu、memory占用率的曲线图，图表保存至chart目录下
        self.utils = AdbCmder()
        self.sno = sno
        if times is None or time == "":
            self.times = 30        #top次数
        else:
            self.times = string.atoi(times)
            if self.times < 15 and self.times > 0:
                self.times = 20
        if pkg_name is None or pkg_name == "":
            self.pak_name = self.utils.get_current_package_name(sno)
        else:
            self.pkg_name = pkg_name          # 设备当前运行应用的包名

    # 获取cpu、mem占用
    def top(self):
        cpu = []
        mem = []
        top_info = self.utils.shell(self.sno, "top -n %s | findstr %s$" %(str(self.times), self.pkg_name)).stdout.readlines()
    #  PID PR CPU% S #THR VSS RSS PCY UID Name
        for info in top_info:
            # temp_list = del_space(info)
            temp_list = info.split()
            cpu.append(temp_list[2])
            mem.append(temp_list[6])
        return cpu, mem

    # 绘制线性图表，具体接口的用法查看ChartDirecto的帮助文档
    def line_chart(self, data):
        PATH = lambda p: os.path.abspath(p)
        cpu_data = []
        mem_data = []
        # 去掉cpu占用率中的百分号，并转换为int型
        for cpu in data[0]:
            cpu_data.append(string.atoi(cpu.split("%")[0]))
        # 去掉内存占用中的单位K，并转换为int型，以M为单位
        for mem in data[1]:
            mem_data.append(string.atof(mem.split("K")[0])/1024)

        # 横坐标
        labels = []
        for i in range(1, self.times + 1):
            labels.append(str(i))

        # 自动设置图表区域宽度
        if self.times <= 50:
            xArea = self.times * 40
        elif 50 < self.times <= 90:
            xArea = self.times * 20
        else:
            xArea = 1800

        c = XYChart(xArea, 800, 0xCCEEFF, 0x000000, 1)
        c.setPlotArea(60, 100, xArea - 100, 650)
        c.addLegend(50, 30, 0, "arialbd.ttf", 15).setBackground(Transparent)

        c.addTitle("cpu and memery info(%s)" %self.pkg_name, "timesbi.ttf", 15).setBackground(0xCCEEFF, 0x000000, glassEffect())
        c.yAxis().setTitle("The numerical", "arialbd.ttf", 12)
        c.xAxis().setTitle("Times", "arialbd.ttf", 12)

        c.xAxis().setLabels(labels)

        # 自动设置X轴步长
        if self.times <= 50:
            step = 1
        else:
            step = self.times / 50 + 1

        c.xAxis().setLabelStep(step)

        layer = c.addLineLayer()
        layer.setLineWidth(2)
        layer.addDataSet(cpu_data, 0xff0000, "cpu(%)")
        layer.addDataSet(mem_data, 0x008800, "mem(M)")

        path = PATH("%s/chart" %os.getcwd())
        if not os.path.isdir(path):
            os.makedirs(path)

        # 图片保存至脚本当前目录的chart目录下
        c.makeChart(PATH("%s/%s.png" %(path, self.utils.timestamp())))





