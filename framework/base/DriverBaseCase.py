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

from framework import LogObj
from framework import DateTimeManager
from framework import InitBrowser
from framework import FileChecK
from framework import Config
import time
import os


class WebDriverDoBeforeTest():

    def __init__(self):
        self.driver = None
        self.className = None
        self.beforeSuiteStarts = 0
        self.afterSuiteStops = 0
        self.beforeClassStarts = 0
        self.afterClassStops = 0
        self.beforeTestStarts = 0
        self.afterTestStops = 0
        fc = FileChecK()
        boolean = fc.is_has_file("framework.ini")
        if boolean:
            self.projectpath = fc.getProjectPath()
            self.fwInipath = fc.get_fileabspath()
        self.logger = LogObj()
        self.capturePath = os.path.join(self.projectpath,Config(self.fwInipath).get("capturePath", "capturePath"))

    def getDriverTooler(self,initbrowsername,baseURL):
        initbrowser = InitBrowser()
        initbrowser.beforeTestInitBrowser(initbrowsername,baseURL)
        self.driver = initbrowser.getWebDriver()
        return self.driver

    def beforeSuite(self):
        begins = DateTimeManager().formatedTime("%Y-%m-%d %H:%M:%S:%f")
        self.beforeSuiteStarts = time.time()
        self.logger.info("======" + begins + "：测试集开始======")

    def afterSuite(self):
        ends = DateTimeManager().formatedTime("%Y-%m-%d %H:%M:%S:%f")
        self.afterSuiteStops = time.time()
        self.logger.info("======" + ends + "：测试集结束======")
        self.logger.info("======本次测试集运行消耗时间 "+str(self.afterSuiteStops - self.beforeSuiteStarts) + " 秒！======");

    def beforeClass(self):
        begins = DateTimeManager().formatedTime("%Y-%m-%d %H:%M:%S:%f")
        self.beforeClassStarts = time.time()
        self.logger.info("======" + str(begins) + "：测试【" + str(self.className) + "】开始======");

    def afterClass(self):
        ends = DateTimeManager().formatedTime("%Y-%m-%d %H:%M:%S:%f")
        self.afterClassStops = time.time()
        self.logger.info("======" + str(ends) + "：测试【" + str(self.className) + "】结束======");
        self.logger.info("======本次测试运行消耗时间 " + str(self.afterClassStops-self.beforeClassStarts)+ " 秒！======")

    def beforeTest(self, methodName) :
        begins = DateTimeManager().formatedTime("%Y-%m-%d %H:%M:%S:%f");
        self.beforeTestStarts = time.time()
        self.logger.info("======" + begins + "：案例【" + str(self.className) + "." + methodName+ "】开始======")

    def afterTest(self,methodName, isSucceed):
        ends = DateTimeManager().formatedTime("%Y-%m-%d %H:%M:%S:%f")
        captureName = ""
        if (isSucceed):
            self.logger.info("案例 【" + str(self.className) + "." + methodName + "】 运行通过！")
        else:
            dateTime = DateTimeManager().formatedTime("-%Y%m%d-%H%M%S%f")
            captureName = self.capturePath+ str(self.className)+"."+methodName+str(dateTime)+".png"
            self.captureScreenshot(captureName)
            self.logger.error("案例 【" + str(self.className) + "." + methodName+ "】 运行失败，请查看截图快照：" + captureName)
        self.logger.info("======" + ends + "：案例【" + str(self.className) + "." + methodName+ "】结束======")
        afterTestStops = time.time()
        self.logger.info("======本次案例运行消耗时间 " + str(afterTestStops - self.beforeTestStarts) + " 秒！======");
        return captureName;

    '''
     * 截取屏幕截图并保存到指定路径
     * @param name：保存屏幕截图名称
     * @return 无
     '''
    def capture(self,name):
        time.sleep(3)
        dateTime = DateTimeManager().formatedTime("-%Y%m%d-%H%M%S-%f")
        captureName = self.capturePath+name+dateTime+".png"
        self.captureScreenshot(captureName)
        self.logger.debug("请查看截图快照：" + captureName)

    '''
     * 截取屏幕截图并保存到指定路径
     * @param filepath:保存屏幕截图完整文件名称及路径
     * @return 无
    '''
    def captureScreenshot(self, filepath):
        try:
            self.driver.get_screenshot_as_file(filepath)
        except Exception as e:
            self.logger.error("保存屏幕截图失败，失败信息："+str(e))

    '''
     * public method for handle assertions and screenshot.
     * @param isSucceed:if your operation success
     * @throws RuntimeException
    '''
    def operationCheck(self, methodName, isSucceed):
        if (isSucceed):
            self.logger.info("method 【" + methodName + "】 运行通过！");
        else:
            self.logger.error("method 【" + methodName + "】 运行失败！");
