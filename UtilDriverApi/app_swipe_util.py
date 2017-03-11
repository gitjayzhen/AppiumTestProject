#!/usr/bin/env python
# -*- coding:utf8 -*-

'''
函数封装：
1.appium的滑动api：swipe(int startx,int starty,int endx,int endy,duration)
x:开始的坐标点到终止的坐标点
y:开始的坐标点到终止的坐标点
duration:滑动的时间（默认：5毫秒）
'''

class AppSwipeUtil():

    def __init__(self,driver):
        self.driver = driver

    #获取屏幕的尺寸
    def get_screen_size(self,driver):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return (x,y)

    #操作屏幕向上滑动
    def swipe_up(self,driver,duration_time):
        size_screen = self.get_screen_size(driver)
        x_start = int(size_screen[0] * 0.5)
        x_end = x_start
        y_start = int(size_screen[1] * 0.75)
        y_end = int(size_screen[0] * 0.25)
        self.driver.swipe(x_start,y_start,x_end,y_end,duration_time)
        print "log:action swipe up:(%d,%d)-(%d,%d)"%(x_start,y_start,x_end,y_end)

    #操作屏幕向下滑动
    def swipe_down(self,driver,duration):
        size_screen = self.get_screen_size(driver)
        x_start = int(size_screen[0] * 0.5)
        x_end = x_start
        y_start = int(size_screen[1] * 0.25)
        y_end = int(size_screen[0] * 0.75)
        self.driver.swipe(x_start,y_start,x_end,y_end,duration_time)
        print "log:action swipe down:(%d,%d)-(%d,%d)"%(x_start,y_start,x_end,y_end)

    #操作屏幕向左←滑动
    def swipe_left(self,driver,duration_time):
        size_screen = self.get_screen_size(driver)
        y_start = int(size_screen[0] * 0.5)
        y_end = x_start
        x_start = int(size_screen[1] * 0.75)
        x_end = int(size_screen[0] * 0.25)
        self.driver.swipe(x_start,y_start,x_end,y_end,duration_time)
        print "log:action swipe left:(%d,%d)-(%d,%d)"%(x_start,y_start,x_end,y_end)

    #操作屏幕向右→滑动
    def swipe_right(self,driver,duration_time):
        size_screen = self.get_screen_size(driver)
        y_start = int(size_screen[0] * 0.5)
        y_end = x_start
        x_start = int(size_screen[1] * 0.25)
        x_end = int(size_screen[0] * 0.75)
        self.driver.swipe(x_start,y_start,x_end,y_end,duration_time)
        print "log:action swipe right:(%d,%d)-(%d,%d)"%(x_start,y_start,x_end,y_end)

