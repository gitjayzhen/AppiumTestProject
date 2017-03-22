# -*- coding: utf-8 -*-

class SriptException(Exception):
    def __init__(self, str):
        self.str = str

    def _str_(self):
        return self.str
