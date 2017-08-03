#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@version: python2.7
@author: ‘jayzhen‘
@contact: jayzhen_testing@163.com
@site: https://github.com/gitjayzhen
@software: PyCharm Community Edition
@time: 2017/3/29  13:12
"""
import json
from com.framework.utils.fileutils.FileCheckAndGetPath import FileChecKController
from com.framework.utils.reporterutils.LoggingUtil import LoggingController


class JsonParser(object):
    def __init__(self):
        self.json_obj = None
        self.fc = FileChecKController()
        if self.fc.is_has_file("android_devices_info.json"):
            self.json_file_path = self.fc.get_fileabspath()
        self.log4py = LoggingController()

    def load_json(self,json_file_path):
        fin = open(json_file_path,"r")
        try:
            json_obj = json.load(fin)
            self.log4py.info("加载了%s文件"%json_file_path)
        except ValueError, e:
            json_obj = {}
        fin.close()
        return json_obj

    def get_value_with_key(self, json_key):
        pass

    def put_key_value(self,dict_data):
        try:
            json_obj = self.load_json(self.json_file_path)
            n = 0
            for k in dict_data:
                if not json_obj.has_key(k):
                    json_obj[k] = dict_data[k]
                    n += 1
            if n == 0 :
                print "该设备的数据已存在"
                return None
            self.log4py.info(dict_data)
            with open(self.json_file_path,'w+') as json_f_obj:
                json_f_obj.write(json.dumps(json_obj,sort_keys=True,indent =4,separators=(',', ': '),encoding="gbk",ensure_ascii=True))
        except Exception,e:
            self.log4py.error("JsomParser func happend error")
        else:
            self.log4py.info("device info collect work has done, go to check json file")

