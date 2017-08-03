#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@version: python2.7
@author: ‘jayzhen‘
@contact: jayzhen_testing@163.com
@site: https://github.com/gitjayzhen
@software: PyCharm Community Edition
@time: 2017/3/29  13:12

1.通过filecheck来查看项目目录下是否有指定文件
2.确定有指定文件后，可以获取文件的绝对路径（一定要保证文件名是正确的）
"""

import datetime
import os
import time
from com.framework.utils.reporterutils.LoggingUtil import LoggingController

class FileChecKController():

    def __init__(self):
        self.__fileabspath = None  #不可访问的
        self.__logger = LoggingController()
    '''
    是否存在指定的文件，路径默认为当前项目的目录
    '''
    def is_has_file(self, filename):
        propath = self.get_project_path()
        boolean = self.is_path_has_file(propath, filename)
        return boolean

    '''
    指定目录下是否存在指定的文件
    '''
    def is_path_has_file(self,path,filename):
        boolean = self.check_has_file(path,filename)
        return boolean

    '''
   扫描指定目录下的所有文件，找到所要找的文件，return True or False
     '''
    def check_has_file(self, path, filename):
        try:
            for filep, dirs, filelist in os.walk(path):
                for fl in filelist:
                    if cmp(fl, filename) == 0:    #这个字符串的比较存在风险，python3不支持，待修改
                        self.__fileabspath = os.path.join(filep, fl)
                        self.__logger.info("查找的%s文件存在" %filename)
                        return True
            return False
        except Exception, e:
            self.__logger.error("check_has_file()方法出现异常",e)

    '''
    获取文件的绝对路径之倩需要check文件是否存在
    '''
    def get_fileabspath(self):
        return self.__fileabspath

    '''
    截取当前项目所有在的路径
    '''
    def get_project_path(self):
        abspath = os.getcwd()
        project_path = abspath.split("src")[0] #当前项目的目录
        return project_path

    '''
    1.在指定文件下，获取所有文件
    2.再获取每个文件的时间，对比后获取文件名（使用内置函数）
    '''
    def get_LatestFile(self):
        pro_path = self.get_project_path()
        rpath = "TestResult\Reports"
        result_dir = os.path.join(pro_path,rpath)
        l = os.listdir(result_dir)  #该目录下的文件list
        #对key进行升序排列（变量fn是每个文件或者文件夹的全称，如果fn是不是文件夹或者是0，那就获取该文件的创建时间，排序后的最后一个文件就是最新的文件了）
        st = l.sort(key=lambda fn: os.path.getmtime(result_dir+"\\"+fn) if not os.path.isdir(result_dir+"\\"+fn) else 0)    #第二句
        d = datetime.datetime.fromtimestamp(os.path.getmtime(result_dir+"\\"+l[-1]))
        fname = l[-1]
        fpath = os.path.join(result_dir, fname)
        self.__logger.debug('last file is ::'+fpath)
        time_end = time.mktime(d.timetuple())
        self.__logger.debug('time_end:%s'%time_end)
        return fpath, fname, result_dir   #fpath:html文件的全目录,fname：最新html文件名,result_dir：html文件当前所处文件夹路径










