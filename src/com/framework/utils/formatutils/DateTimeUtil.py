#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@version: python2.7
@author: ‘jayzhen‘
@contact: jayzhen_testing@163.com
@site: https://github.com/gitjayzhen
@software: PyCharm Community Edition
@time: 2017/3/29  13:12
"""
import time
import datetime
import calendar


class DateTimeManager(object):

    '''
     * 获取系统当前日期和时间并格式化为yyyyMMddHHmmss即类似20110810155638格式
     * @param 无
     * @return 系统当前日期和时间并格式化为yyyyMMddHHmmss即类似20110810155638格式
    '''
    def getCurrentDateTime(self):
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    '''
     * 获取系统当前日期和时间并格式化为yyyyMMddHHmmssSSS即类似20130526002728796格式
     * @param 无
     * @return 系统当前日期和时间并格式化为yyyyMMddHHmmssSSS即类似20130526002728796格式
    '''
    def getDateTime(self):
        return datetime.datetime.now()

    '''
     * 获取系统当前日期并格式化为yyyyMMdd即类似20110810格式
     * @param 无
     * @return 系统当前日期并格式化为yyyyMMdd即类似20110810格式
     '''
    def getCurrentDate(self):
        return datetime.datetime.now().strftime("%Y%m%d")

    '''
     * 获取系统当前时间并格式化为HHmmss即类似155638格式
     * @param 无
     * @return 系统当前时间并格式化为HHmmss即类似155638格式
     '''
    def getCurrentTime(self):
        return datetime.datetime.now().strftime("%H%M%S")

    '''
     * 获取系统当前时间并格式化为HHmmssSSS即类似155039527格式
     * @param 无
     * @return 系统当前时间并格式化为HHmmssSSS即类似155039527格式
    '''
    def getTime(self) :
        return datetime.datetime.now().strftime("%H%M%S%f")
    
    '''
     * 根据自定义格式化获取系统当前时间
     * @param format：时间格式化如yyyy-MM-dd HH:mm:ss:SSS  "%Y%m%d%H%M%S%f"
     * @return 根据自定义格式化返回系统当前时间
     '''
    def formated_time(self, format_time):
        return datetime.datetime.now().strftime(format_time)
    '''
     * get specified time string in specified date format.
     * @param days
     *            days after or before current date, use + and - to add.
     * @param dateFormat
     *            the formatter of date, such as:yyyy-MM-dd HH:mm:ss:SSS.
     '''
    def addDaysByFormatter(self,adddays,dateFormat):
        afteraddtime = datetime.datetime.now() + datetime.timedelta(days=adddays)     
        return time.strftime(afteraddtime,dateFormat)

    '''
     * get specified time string in specified date format.
     * @param months： months after or before current date, use + and - to add.
     * @param dateFormat：the formatter of date, such as:yyyy-MM-dd HH:mm:ss:SSS.
     '''
    def addMonthsByFormatter(self, months,dateFormat):
        d = datetime.datetime.now()
        c = calendar.Calendar()
        year = d.year
        month = d.month
        today = d.day
        if month+months > 12 :
            month = months
            year += 1
        else:
            month += months
        days = calendar.monthrange(year, month)[1]  
        
        if today > days:
            afteraddday = days
        else:
            afteraddday = today
        return datetime.datetime(year,month,afteraddday).strftime(dateFormat)
    '''
     * get specified time string in specified date format.
     * @param years：years after or before current date, use + and - to add.
     * @param dateFormat：the formatter of date, such as:yyyy-MM-dd HH:mm:ss:SSS.
     '''
    def addYearsByFormatter(self, years,dateFormat):
        d = datetime.datetime.now()
        c = calendar.Calendar()
        year = d.year + years
        month = d.month
        today = d.day
        
        days = calendar.monthrange(year, month)[1]  
        
        if today > days:
            afterday = days
        else:
            afterday = today
        return datetime.datetime(year,month,afterday).strftime(dateFormat)

    '''
    * get first day of next month in specified date format.
    * @param dateFormat： the formatter of date, such as:yyyy-MM-dd HH:mm:ss:SSS.
    '''
    def firstDayOfNextMonth(self, dateFormat):
        d = datetime.datetime.now()
        year = d.year
        month = d.month
        if month+1 > 12 :
            month = 1
            year += 1
        else :
            month += 1
        
        return datetime.datetime(year,month,1).strftime(dateFormat)

    '''
     * get first day of specified month and specified year in specified date
     * format.
     * @param year: the year of the date.
     * @param month:the month of the date.
     * @param dateFormat:the formatter of date, such as:yyyy-MM-dd HH:mm:ss:SSS.
    '''
    def firstDayOfMonth(self, year,month, dateFormat):
        return datetime.datetime(year,month,1).strftime(dateFormat)
    
    '''
      get first day of specified month of current year in specified dateformat.
      @param month:the month of the date.
      @param dateFormat:the formatter of date, such as:yyyy-MM-dd HH:mm:ss:SSS.
        '''
    def  firstDayOfMonthThisYear(self,month,dateFormat):
        d = datetime.datetime.now()
        year = d.year
        return datetime.datetime(year,month,1).strftime(dateFormat)

    '''
    get the system current milliseconds.
    '''
    def getMilSecNow(self):
        return time.time()

    
