#!/usr/bin/env python
# -*- coding:UTF-8 -*-
"""
@version: python2.7
@author: ‘dell‘
@contact: jayzhen_testing@163.com
@site: https://github.com/gitjayzhen
@software: PyCharm Community Edition
@time: 2017/3/29  13:12
"""

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from com.framework.utils.fileutils.filecheckandgetpath import FileChecKController
from com.framework.utils.fileutils.configcommonctl import ConfigController
from com.framework.utils.reporterutils.loggingctl import LoggingController

class EmailController():

    def __init__(self):
        self.fc = FileChecKController()
        bools = self.fc.is_has_file("email.ini")
        if bools:
            fp = self.fc.get_fileabspath()
            conf = ConfigController(fp)
            self.smtp_host =conf.get("emails", "smtp_host")    
            self.pop3_host =conf.get("emails", "pop3_host")
            self.receiver = conf.get("emails", "receiver").split(",")
            self.receiver_pa =conf.get("emails", "receiver_pa")
            self.sender =conf.get("emails", "sender")
            self.sender_pa =conf.get("emails", "sender_pa")
        self.log4py = LoggingController()
            
        
    def send_email_is_html(self):
        latestfpath,fname,currentfolder = self.fc.get_LatestFile()
        msgRoot = MIMEMultipart('related')
        ff = open(latestfpath, 'rb')
        message = MIMEText(ff.read(), 'html', 'utf-8')
        ff.close()
        message['From'] = self.sender
        #message['To'] = self.receiver
        subject = '实验室数字化平台-自动化测试报告'
        message['Subject'] = Header(subject, 'utf-8')
        msgRoot.attach(message)
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.smtp_host)
            smtpObj.login(self.sender, self.sender_pa)
            smtpObj.sendmail(self.sender, self.receiver, msgRoot.as_string())
            self.log4py.debug("SendEmail_withFile邮件发送成功")
            smtpObj.close()
        except Exception,e:
            print e
            self.log4py.error("Error: 无法发送邮件::"+str(e))
            
    def send_email_with_file(self):
        #创建一个带附件的实例 related   alternative
        message = MIMEMultipart("related")
        #message['from'] = Header("QA jayzhen <%s>" %self.sender, 'utf-8')
        message['from'] = self.sender
        #message['To'] =  Header("Leader <%s>" %self.receiver, 'utf-8')
        #message['To'] = self.receiver   #群发邮件不能使用
        subject = '实验室数字化平台-自动化测试报告'
        message['Subject'] = Header(subject, 'utf-8')
        #邮件正文内容
        message.attach(MIMEText('<html><br/><h1>基于Spring MVC的实验室数字化平台-自动化测试 V1.0版本 -自动化测试报告</h1><br/><h3>附件报告，请下载！（邮件为自动发送勿回）</h3></html>', 'html', 'utf-8'))
        
        latestfpath,fname,currentfolder= self.fc.get_LatestFile()
        # 构造附件1，传送当前目录下的 test.txt 文件
        with open(latestfpath, 'rb') as f:
            att1 = MIMEText(f.read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename=%s'%fname
        message.attach(att1)
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.smtp_host)
            smtpObj.login(self.sender, self.sender_pa)
            smtpObj.sendmail(self.sender, self.receiver, message.as_string())
            self.log4py.debug("SendEmail_withFile邮件发送成功")
            smtpObj.close()
        except Exception ,e:
            self.log4py.error("Error: 无法发送邮件::"+str(e))
            print e
            
    
    