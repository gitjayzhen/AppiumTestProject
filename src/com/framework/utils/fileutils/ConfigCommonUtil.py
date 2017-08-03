#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@version: python2.7
@author: ‘dell‘
@contact: jayzhen_testing@163.com
@site: https://github.com/gitjayzhen
@software: PyCharm Community Edition
@time: 2017/3/29  13:12

1.对ini配置文件进行读取操作
"""
import sys
import ConfigParser


class ConfigController(object):

    def __init__(self, path):
        self.path = path
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.path)
        
    def get(self, field, key):
        result = ""
        try:
            result = self.cf.get(field, key)
        except Exception as e:
            result = ""
        return result

    def set(self, filed, key, value):
        try:
            self.cf.set(filed, key, value)
            self.cf.write(open(self.path, 'w'))
        except Exception as e:
            return False
        return True

    '''
    备用的
    '''
    def read_config(self,config_file_path, field, key): 
        cf = ConfigParser.ConfigParser()
        try:
            cf.read(config_file_path)
            result = cf.get(field, key)
        except:
            sys.exit(1)
        return result

    def write_config(self,config_file_path, field, key, value):
        cf = ConfigParser.ConfigParser()
        try:
            cf.read(config_file_path)
            cf.add_section(field)
            cf.set(field, key, value)
            cf.write(open(config_file_path,'w'))
        except:
            sys.exit(1)
        return True


