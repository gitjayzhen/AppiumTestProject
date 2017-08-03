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

class ScriptException(Exception):
    def __init__(self, str_param):
        self.str_param = str_param

    def _str_(self):
        return self.str_param

