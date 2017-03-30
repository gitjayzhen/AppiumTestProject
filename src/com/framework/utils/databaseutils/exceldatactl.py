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
from com.framework.logging.Recoed_Logging import LogObj
from com.framework.util.ConfigCommonManager import Config
from com.framework.util.FileCheckAndGetPath import FileChecK
import datetime
class ExcelManager():
    
    def __init__(self,excelfilename):
        self.excelfilename = excelfilename
        fc = FileChecK()
        boolean = fc.is_has_file(excelfilename)
        if boolean:
            self.excel_path = fc.get_fileabspath()
        self.logger = LogObj()

    def readexcel(self,excel_sheet_name):
        
        #打开目标excel文件  r--读，w--写（覆盖），a--追加写
        xlsdata = xlrd.open_workbook(self.excel_path,"rb")
        table = xlsdata.sheet_by_name(excel_sheet_name)  #打开sheet页
        self.logger.debug("打开的%s文件中的sheet页" %(self.excelfilename))
        
        return table   # 将指定的sheet页对象返回给调用者
    
    #############################################################    
        
    def writexcel(self,row,column,value):
        xdata = xlrd.open_workbook(self.excel_path,"rb") #只能是xls文件
        copy_Sheet = copy(xdata)           #copy，并对附件进行操作
        writeXLS = copy_Sheet.get_sheet(0)  #得到附件中的sheet页
        writeXLS.write(row,column,value)          #将测试的结果追加到附件中sheet页中每一行的后面
        copy_Sheet.save(self.excel_path)   #覆盖保存（注意编码错误）

'''        
t = ExcelManager("UsersLogin.xlsx")
tes_xls_data = t.readexcel("users")  #得到sheet页
nrows = tes_xls_data.nrows
print "------ excel中的测试用例条数是：",nrows-1    #excel中 的数据行数从1行开始
for i in range(1,nrows):       #for循环式，默认从0--n-1
    print "------ 这是第：",i," 条用例"
    print tes_xls_data.cell(i,0).value
    print tes_xls_data.cell(i,1).value   
''' 
        
        
        