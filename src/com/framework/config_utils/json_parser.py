#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
from device_info import DeviceInfo
class JsonParser():
    def __init__(self):
        self.json_obj = None
        self.json_file_path = os.path.join(os.path.dirname(os.getcwd()),"logs\\android_devices_info.json")

    def load_json(self,json_file_path):
        fin = open(json_file_path,"r")
        try:
            json_obj = json.load(fin)
        except ValueError,e:
            json_obj = {}
        fin.close()
        return json_obj

    def get_value_with_key(self,json_key):
        return value

    def put_key_value(self,dict_data):
        try:
            json_obj = self.load_json(self.json_file_path)
            n = 0
            for k in dict_data:
                if not json_obj.has_key(k):
                    json_obj[k] = dict_data[k]
                    n += 1
            if n == 0 :
                print "数据存在"
                return None
            with open(self.json_file_path,'w+') as json_f_obj:
                json_f_obj.write(json.dumps(json_obj,sort_keys=True,indent =4,separators=(',', ': '),encoding="gbk",ensure_ascii=True))
        except Exception,e:
            print e
        else:
            print "device info collect work has done, go to check json file"

if __name__ == '__main__':
    and_obj  = DeviceInfo()
    json_paser =  JsonParser()
    json_paser.put_key_value(and_obj.get_devices_as_dict())
