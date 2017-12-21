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

import os
import time
import re


# 返回函数式方法
def file_end_with(*endstring):
    ends = endstring

    def run(s):
        f = map(s.endswith, ends)
        if True in f:
            return s
    return run


def san_path(abs_path, end_string):
    backfunc= file_end_with(end_string)
    for filepath, dirs, filelist in os.walk(abs_path):
        if not re.search("\.git", filepath):
            f_file = filter(backfunc, filelist)
            for i in f_file:
                print os.path.join(filepath, i)


if __name__ == '__main__':
    # path = os.getcwd().split("AppiumTestProject")[0]
    # san_path(path, '.py')
    f = file_end_with("json")
    print f("str.json")










