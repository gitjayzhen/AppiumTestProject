#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
@version: python2.7
@author: ‘dell‘
@contact: jayzhen_testing@163.com
@site: https://github.com/gitjayzhen
@software: PyCharm Community Edition
@time: 2017/3/29  13:12
先抽象后具体，保证整体的流程，在细化过程中的操作
"""

import mysqldb
from com.framework.utils.fileutils.ConfigCommonUtil import ConfigController
from com.framework.utils.fileutils.FileCheckAndGetPath import FileChecKController
from com.framework.utils.reporterutils.LoggingUtil import LoggingController


class MySQLController(object):
    
    def __init__(self):
        self.logger = LoggingController()
        self.fc = FileChecKController()
        boolean = self.fc.is_has_file("db.ini")
        if boolean:
            self.inipath = self.fc.get_fileabspath()
        self.conf = ConfigController(self.inipath)
        self.host = str(self.conf.get("dbset", "host"))
        self.port = int(self.conf.get("dbset", "port"))
        self.user = str(self.conf.get("dbset", "user"))
        self.passwd = str(self.conf.get("dbset", "passwd"))
        self.db = str(self.conf.get("dbset", "db"))
        self.charset = str(self.conf.get("dbset", "charset"))
        self.conn = mysqldb.Connect(self.host, self.user, self.passwd, self.db, self.port, self.charset)
        self.logger.debug("数据库初始化完成"+self.host+str(self.port)+self.db+self.charset)
   
    def execute_select(self, sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            self.logger.debug("check_acct_available :" +sql)
            res = cursor.fetchall()
            if len(res) < 1:
                self.logger.error("%s执行查询内容不存在"%sql)
            return res
        finally:
            cursor.close()
        return None
    
    def execute_add_one(self, sql):
        cursor = self.conn.cursor()   #操作数据库的游标
        try:
            cursor.execute(sql)   #执行sql语句
            if cursor.rowcount == 1:
                self.logger.debug("%s添加成功"%sql)
                self.conn.commit()  #执行成功后向数据库进行提交
                return True 
        except Exception, e:
            self.conn.rollback()
            self.logger.error("插入数据出现错误"+str(e))
        finally:
            cursor.close()
        return False
    
    def execute_delete(self,sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            if cursor.rowcount==1:
                self.logger.debug("%s删除成功"%sql)
                self.conn.commit()
                return True
        except Exception,e:
            self.conn.rollback()
            self.logger.error("删除数据出现错误"+str(e))
        finally:
            cursor.close()
        return False
    
    def execute_update(self,sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            if cursor.rowcount==1:
                self.logger.debug("%s更新失败" % sql )
                self.conn.commit()
                return True
        except Exception,e:
            self.conn.rollback()
            self.logger.error("更新数据出现错误"+str(e))
        finally:
            cursor.close()
        return False
    
    def execute_conn_close(self):
        try:
            self.conn.close()
        except Exception as e:
            self.logger.error("执行关闭数据库链接出现错误"+str(e))
