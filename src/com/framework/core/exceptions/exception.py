#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ScriptException(Exception):
    def __init__(self, str_param):
        self.str_param = str_param

    def _str_(self):
        return self.str_param

