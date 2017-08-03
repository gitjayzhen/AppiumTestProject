#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
python实现读取Excel文件中的内容
准备：环境中必须有相关的包
1.找到文件所在路径
2.打开文件
3.获取内容行数
4.读取指定位子的数据
"""

import xlrd
from xlutils.copy import copy
import os
from com.framework.utils.reporterutils.LoggingUtil import LoggingController
from com.framework.utils.fileutils.FileCheckAndGetPath import FileChecKController
import datetime


class ExcelManager(object):
    
    def __init__(self, excelfilename):
        self.excelfilename = excelfilename
        fc = FileChecKController()
        boolean = fc.is_has_file(excelfilename)
        if boolean:
            self.excel_path = fc.get_fileabspath()
        self.log4py = LoggingController()

    def read_excel(self, excel_sheet_name):
        
        """打开目标excel文件  r--读，w--写（覆盖），a--追加写"""
        xls_data = xlrd.open_workbook(self.excel_path, "rb")
        table = xls_data.sheet_by_name(excel_sheet_name)  #打开sheet页
        self.log4py.debug("打开的%s文件中的sheet页" % self.excelfilename)
        return table   # 将指定的sheet页对象返回给调用者
        
    def writ_excel(self, row, column, value):
        x_data = xlrd.open_workbook(self.excel_path, "rb") #只能是xls文件
        copy_sheet = copy(x_data)           #copy，并对附件进行操作
        write_xls = copy_sheet.get_sheet(0)  #得到附件中的sheet页
        write_xls.write(row, column, value)          #将测试的结果追加到附件中sheet页中每一行的后面
        copy_sheet.save(self.excel_path)   #覆盖保存（注意编码错误）
