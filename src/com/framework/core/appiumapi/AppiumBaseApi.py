#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@version: python2.7
@author: ‘jayzhen‘
@license: Apache Licence 
@contact: 2431236868@qq.com
@site: http://www.jayzhen.com
@software: PyCharm
@file: AppiumBaseApi.py
@time: 2017/3/28  23:32
"""
from appium.webdriver.common.touch_action import TouchAction
from com.framework.core.adb.AdbCommand import AdbCmder
from appium.webdriver.common.mobileby import MobileBy as By
from com.framework.base.GetAllPathCtrl import GetAllPathController
from com.framework.utils.reporterutils.LoggingUtil import LoggingController
from com.framework.utils.formatutils.DateTimeUtil import DateTimeManager
import os
import re
import time
import random


PATH = lambda a: os.path.abspath(a)


class AppiumDriver(object):

    def __init__(self, driver):
        self.android = AdbCmder()
        self.log4py = LoggingController()
        self.driver = driver
        self.taction = TouchAction(self.driver)
        self.path_get = GetAllPathController()
        self.actions = []
        self.xml_file_path = self.path_get.get_dumpxml_path()
        self.pattern = re.compile(r"\d+")
        self.capturePath = self.path_get.get_capture_path()

    def is_displayed(self, by, value):
        is_displayed = False
        try:
            is_displayed = self.driver.find_element(by, value).is_displayed()
            self.log4py.debug("element [ " + str(value) + " ] displayed? " + str(is_displayed))
        except Exception, e:
            self.log4py.error("element元素没有点位到"+str(e))
        return is_displayed

    def is_enabled(self, by, value):
        '''
         * rewrite the isEnabled method, the element to be find  </BR>
         * 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
         * @param ：the locator you want to find the element
         * @return the bool value of whether is the WebElement enabled    '''
        isEnabled = self.driver.find_element(by, value).is_enabled()
        self.log4py.debug("element [ " + str(by) + " ] enabled? "
                + (isEnabled))
        return isEnabled

    def is_element_present(self, by, value, timeout):
        isSucceed = False
        self.log4py.debug("find element [" + value + "]")
        timeBegins = time.time()
        while(time.time() - timeBegins <= timeout):
            try:
                self.driver.find_element(by,value)
                isSucceed = True
                self.log4py.debug("find element [" + value+ "] success")
                break
            except Exception,e:
                self.log4py.error(e)
            self.pause(self.pauseTime)
        self.operationCheck("isElementPresent", isSucceed)
        return isSucceed

    def is_alert_exists(self,timeout):
        '''
         * judge if the alert is present in specified seconds</BR>
         * 在指定的时间内判断弹出的对话框（Dialog）是否存在。
         * @param timeout:timeout in seconds
             '''
        isSucceed = False
        timeBegins = time.time()
        while(time.time() - timeBegins <= timeout * 1000):
            try:
                self.driver.switch_to_alert()
                isSucceed = True
                break
            except Exception,e:
                self.log4py.error(e)
        self.operationCheck("isAlertExists", isSucceed)
        return isSucceed

    def find_element_by_want(self, by, value, timeout):
        """
        通过元素名称定位单个元素
        usage: findElementByName(u"设置")
        """
        is_succeed = False
        element = None
        time_begins = time.time()
        if timeout is None or timeout == "":
            timeout = 3
        while time.time() - time_begins <= timeout:
            try:
                element = self.driver.find_element(by, value)
                is_succeed = True
                self.log4py.debug("find element [" + str(value) + "] success")
                break
            except Exception, e:
                self.log4py.error(str(e))
                self.log4py.debug("find element [" + str(value) + "] failure")
        self.operation_check("find_element_by_want", is_succeed)
        return element

    def find_elements_by_want(self, by, value, timeout):
        """
        通过元素名称定位单个元素
        usage: findElementByName(u"设置")
        """
        is_succeed = False
        self.log4py.debug("find elements [" + str(value) + "]")
        elements = None
        time_begins = time.time()
        while (time.time() - time_begins) <= timeout:
            try:
                elements = self.driver.find_elements(by, value)
                is_succeed = True
                self.log4py.debug("find elements [" + str(value) + "] success")
                break
            except Exception, e:
                self.log4py.error(e)
        self.operation_check("find_elements", is_succeed)
        return elements

    def is_element_checked_by_want(self, by, name):
        """
        通过元素名称判断checked的布尔值，返回布尔值列表
        """
        element = self.driver.__getattribute__()
        return self.__checked("text", name)

    def is_elements_checked_by_want(self, id):
        """
        通过元素id判断checked的布尔值，返回布尔值列表
        """
        return self.__checked("resource-id", id)

    def is_selected(self, by, value):
        '''
         * rewrite the isSelected method, the element to be find  </BR>
         * 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
         * @param :the locator you want to find the element
         * @return the bool value of whether is the WebElement selected    '''
        is_selected = self.driver.find_element(by, value).is_selected()
        self.log4py.debug("element [ " + value + " ] selected? "+ str(is_selected))
        return is_selected

    def do_pause(self, millisecond):
        try:
            time.sleep(millisecond)
        except Exception, e:
            self.log4py.error("pause error:"+str(e))

    def get(self, url, actionCount):
        '''
         * rewrite the get method, adding user defined log</BR>
         * 地址跳转方法，使用WebDriver原生get方法，加入失败重试的次数定义。
         * @param url: the url you want to open.
         * @param actionCount:retry: times when load timeout occuers.
        '''
        isSucceed = False
        for i in range(actionCount):
            try:
                self.driver.get(url)
                self.__log4py.debug("navigate to url [ " + url + " ]")
                break
            except Exception,e:
                self.__log4py.error(e)
        self.operationCheck("get", isSucceed)

    def do_navigate_back(self):
        '''
         * navigate back</BR> 地址跳转方法，与WebDriver原生navigate.back方法内容完全一致。
             '''
        self.driver.back()
        self.log4py.debug("navigate back")

    def do_navigate_forward(self):
        '''
         * navigate forward</BR> 地址跳转方法，与WebDriver原生navigate.forward方法内容完全一致。
        '''
        self.driver.forward()
        self.log4py.debug("navigate forward")

    def get_current_activity(self):
        """
        TypeError: 'unicode' object is not callable 是因为方法掉用加了括号
        """
        status = self.driver.current_activity
        self.log4py.debug("current activity is :" + str(status))
        return status

    def get_current_url(self):
        '''
         * rewrite the getCurrentUrl method, adding user defined log</BR>
         * 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
         * @return the url on your current session    '''
        url = self.driver.current_url()
        self.log4py.debug("current page url is :" + url)
        return url

    def get_window_handles(self):
        '''
         * rewrite the getWindowHandles method, adding user defined log</BR>
         * 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。'
         * @return the window handles set    '''
        handles = self.driver.window_handles()
        self.log4py.debug("window handles count are:" + len(handles))
        self.log4py.debug("window handles are: " + handles)
        return handles

    def get_window_handle(self):
        '''
         * rewrite the getWindowHandle method, adding user defined log</BR>
         * 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
         * @return the window handle     '''
        handle = self.driver.current_window_handle()
        self.debug("current window handle is:" + handle)
        return handle

    def get_page_source(self):
        '''
         * rewrite the getPageSource method, adding user defined log</BR>
         * 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
         * @return the page source     '''
        source = self.driver.page_source()
        #log4py.debug("get PageSource : [ " + source + " ]")
        return source

    def get_tag_name(self, by, value):
        '''
         * rewrite the getTagName method, find the element   and get its tag
         * name</BR> 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
         * @param 
         *            the locator you want to find the element
         * @return the tagname     '''
        tag_name = self.driver.find_element(by, value).tag_name
        self.log4py.debug("element [ " + str(by) + " ]'s TagName is: "+ tag_name)
        return tag_name

    def get_text(self, by, value):
        '''  * rewrite the getText method, find the element   and get its own
         * text</BR> 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
         * @param :the locator you want to find the element
         * @return the text     '''
        text = self.driver.find_element(by, value).text
        self.log4py.debug("element [ " + value + " ]'s text is: " + text)
        return text

    def get_attribute(self, by, value, attribute_name):
        '''
         * rewrite the getAttribute method, find the element   and get its
         * attribute value</BR> 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
         * @param :the locator you want to find the element
         * @param attributeName:the name of the attribute you want to get
         * @return the attribute value     '''
        value = self.driver.find_element(by, value).get_attribute(attribute_name)
        self.log4py.debug("element [ " + str(by) + " ]'s " + attribute_name + "is: " + value)
        return value

    def webList_random_select_by_option(self,by,value,timeout):
        isSucceed = False
        timeBegins = time.time()
        while time.time() - timeBegins <= timeout:
            try:
                webselect = self.driver.find_element(by, value)
                selectElement = (webselect)
                ooptions = selectElement.options
                ooption = random.choice(ooptions)
                itemValue = ooption.get_attribute("value")
                selectElement.select_by_value(itemValue)
                isSucceed = True
                self.log4py.debug("item selected by item value [ " + itemValue+ " ] on [ " + str(by) + " ]")
                break
            except Exception,e:
                self.log4py.error(e)
            self.pause(self.pauseTime)
        self.operationCheck("webList_RandomSelectByOption", isSucceed)

    def select_by_value(self, by, value, itemValue, timeout):
        isSucceed = False
        try:
            if (self.isElementPresent(by,value, timeout)):
                element = self.driver.find_element(by, value)
                select = (element)
                select.select_by_value(itemValue)
                self.log4py.debug("item selected by item value [ " + itemValue+ " ] on [ " + value + " ]")
                isSucceed = True
        except Exception,e:
            self.log4py.error(e)
        self.operationCheck("selectByValue", isSucceed)

    def scrollbar_slide_to_bottom(self, element):
        '''将页面滚动条拖到底部
        js="var q=document.documentElement.scrollTop=10000" '''
        js = "var q=document.getElementById('%s').scrollTop=10000" % element
        self.driver.execute_script(js)
        time.sleep(3)
        self.log4py.debug("将元素%s滑动到底部" %element)

    def accept_alert(self):
        try:
            self.driver.switch_to_alert().accept()
            self.log4py.debug("切换到弹窗，并点击确定按钮")
        except Exception, e:
            self.log4py.error("接受弹窗，出现异常："+str(e))

    def get_screen_size(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return (x, y)

    def do_clear(self, element):
        '''
         * rewrite the clear method, adding user defined log</BR>
         * 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
         * @param element:the webelement you want to operate    '''
        element.clear()
        self.log4py.debug("element [ " + element + " ] cleared")

    def do_click(self, by, value, times=3):
        '''
         * rewrite the click method, adding user defined log</BR>
         * 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
         * @param element:the webelement you want to operate    '''
        element = self.find_element_by_want(by,value,times)
        if element is None:
            self.log4py.debug("没有找到对应的元素：{}".format(str(value)))
            return
        element.click()
        self.log4py.debug("click on element [ " + str(element) + " ] ")

    def do_sendkeys(self, by, value, txt):
        element = self.find_element_by_want(by, value, 3)
        if element is None:
            self.log4py.debug("没有找到对应的元素：{}".format(str(value)))
            return
        element.send_keys(txt)
        self.log4py.debug("send key to element [ " + str(element) + " ] ")

    def do_swipe_up(self, driver, duration_time):
        # 操作屏幕向上滑动
        size_screen = self.get_screen_size(driver)
        x_start = int(size_screen[0] * 0.5)
        x_end = x_start
        y_start = int(size_screen[1] * 0.75)
        y_end = int(size_screen[0] * 0.25)
        self.driver.swipe(x_start, y_start, x_end, y_end, duration_time)
        print "log:action swipe up:(%d,%d)-(%d,%d)" % (x_start, y_start, x_end, y_end)

    # 操作屏幕向下滑动
    def do_swipe_down(self, driver, duration_time):
        size_screen = self.get_screen_size(driver)
        x_start = int(size_screen[0] * 0.5)
        x_end = x_start
        y_start = int(size_screen[1] * 0.25)
        y_end = int(size_screen[0] * 0.75)
        self.driver.swipe(x_start, y_start, x_end, y_end, duration_time)
        print "log:action swipe down:(%d,%d)-(%d,%d)" % (x_start, y_start, x_end, y_end)

    # 操作屏幕向左←滑动
    def do_swipe_left(self, driver, duration_time):
        size_screen = self.get_screen_size(driver)
        y_start = int(size_screen[0] * 0.5)
        y_end = y_start
        x_start = int(size_screen[1] * 0.75)
        x_end = int(size_screen[0] * 0.25)
        self.driver.swipe(x_start, y_start, x_end, y_end, duration_time)
        print "log:action swipe left:(%d,%d)-(%d,%d)" % (x_start, y_start, x_end, y_end)

    # 操作屏幕向右→滑动
    def do_swipe_right(self, driver, duration_time):
        size_screen = self.get_screen_size(driver)
        y_start = int(size_screen[0] * 0.5)
        y_end = y_start
        x_start = int(size_screen[1] * 0.25)
        x_end = int(size_screen[0] * 0.75)
        self.driver.swipe(x_start, y_start, x_end, y_end, duration_time)
        print "log:action swipe right:(%d,%d)-(%d,%d)" % (x_start, y_start, x_end, y_end)

    def do_tap_element(self, elemnt):
        """Perform a tap action on the element
        :Args:
         - element - the element to tap
         - x - (optional) x coordinate to tap, relative to the top left corner of the element.
         - y - (optional) y coordinate. If y is used, x must also be set, and vice versa
        :Usage:
        """
        self.taction.tap(elemnt, 10, 10).perform()
        self.log4py.info("appium driver do touch action at element:%s" % (str(elemnt)))

    def do_press(self, el=None, x=None, y=None):
        """Begin a chain with a press down action at a particular element or point
        """
        return self

    def do_long_press(self, el, x, y, duration=1000):
        """Begin a chain with a press down that lasts `duration` milliseconds
        """
        self.taction.press(el, x, y, duration).release().perform()

    def do_wait(self, ms=0):
        """Pause for `ms` milliseconds.
        """
        return self

    def do_move_to(self, el, x, y):
        """Move the pointer from the previous point to the element or point specified
        press(el0).moveTo(el1).release()
        """
        self.taction.move_to(el, x, y)

    def do_release(self):
        """End the action by lifting the pointer off the screen
        """
        self.driver.release()

    def do_perform(self):
        """Perform the action by sending the commands to the server to be operated upon
        """
        # get rid of actions so the object can be reused
        pass

    def do_pinch(self,el):
        '''
        Places two fingers at the edges of the screen and brings them together. 在 0% 到 100% 内双指缩放屏幕，
        '''
        self.driver.pinch(element=el)

    def do_zoom(self, el):
        '''
        放大屏幕 在 100% 以上放大屏幕
        '''
        self.driver.zoom(element=el)

    def do_shake(self):
        '''
        模拟设备摇晃
        '''
        self.driver.shake()

        # convenience method added to Appium (NOT Selenium 3)

    def do_scroll(self, origin_el, destination_el):
        """Scrolls from one element to another
        :Args:
         - originalEl - the element from which to being scrolling
         - destinationEl - the element to scroll to
        :Usage:
            appium_driver.scroll(el1, el2)
        """
        return self

        # convenience method added to Appium (NOT Selenium 3)

    def do_drag_and_drop(self, origin_el, destination_el):
        """Drag the origin element to the destination element
        :Args:
         - originEl - the element to drag
         - destinationEl - the element to drag to
        """
        self.driver.drag_and_drop(origin_el, destination_el)

        # convenience method added to Appium (NOT Selenium 3)

    def do_flick(self, start_x, start_y, end_x, end_y):
        """Flick from one point to another point.
        :Args:
         - start_x - x-coordinate at which to start
         - start_y - y-coordinate at which to start
         - end_x - x-coordinate at which to stop
         - end_y - y-coordinate at which to stop
        :Usage:
            appium_driver.flick(100, 100, 100, 400)
        """
        return self.driver.flick(start_x, start_y, end_x, end_y)

    def capture_screenshot(self, filepath):
        '''* 截取屏幕截图并保存到指定路径
         * @param filepath:保存屏幕截图完整文件名称及路径
         * @return 无    '''
        try:
            self.driver.get_screenshot_as_file(filepath)
        except Exception, e:
            self.log4py.error("保存屏幕截图失败，失败信息："+ str(e))

    def operation_check(self, method_name, is_succeed):
        '''
         * public method for handle assertions and screenshot.
         * @param isSucceed:if your operation success    '''
        if is_succeed:
            self.log4py.info("method 【" + method_name + "】 运行通过！")
        else:
            date_time = DateTimeManager().formated_time("-%Y%m%d-%H%M%S%f")
            capture_name = self.capturePath+method_name+date_time+".png"
            self.capture_screenshot(capture_name)
            self.log4py.error("method 【" + method_name + "】 运行失败，请查看截图快照："+ capture_name)

    @property
    def get_contexts(self):
        """
        Returns the contexts within the current session.
        :Usage:
            driver.contexts
        """
        return self.driver.contexts

    @property
    def get_current_context(self):
        """
        Returns the current context of the current session.
        :Usage:
            driver.current_context
        """
        return self.driver.current_context

    @property
    def get_context(self):
        """
        Returns the current context of the current session.
        :Usage:
            driver.context
        """
        return self.current_context

    def find_element_by_android_uiautomator(self, uia_string):
        """Finds element by uiautomator in Android.
        :Args:
         - uia_string - The element name in the Android UIAutomator library
        :Usage:
            driver.find_element_by_android_uiautomator('.elements()[1].cells()[2]')
        """
        return self.find_element_by_want(by=By.ANDROID_UIAUTOMATOR, value=uia_string)

    def find_elements_by_android_uiautomator(self, uia_string):
        """Finds elements by uiautomator in Android.
        :Args:
         - uia_string - The element name in the Android UIAutomator library
        :Usage:
            driver.find_elements_by_android_uiautomator('.elements()[1].cells()[2]')
        """
        return self.find_elements(by=By.ANDROID_UIAUTOMATOR, value=uia_string)

    def find_element_by_accessibility_id(self, id):
        """Finds an element by accessibility id.
        :Args:
         - id - a string corresponding to a recursive element search using the
         Id/Name that the native Accessibility options utilize
        :Usage:
            driver.find_element_by_accessibility_id()
        """
        return self.find_element_by_want(by=By.ACCESSIBILITY_ID, value=id)

    def find_elements_by_accessibility_id(self, id):
        """Finds elements by accessibility id.
        :Args:
         - id - a string corresponding to a recursive element search using the
         Id/Name that the native Accessibility options utilize

        :Usage:
            driver.find_elements_by_accessibility_id()
        """
        return self.find_elements(by=By.ACCESSIBILITY_ID, value=id)

    def create_web_element(self, element_id):
        """
        Creates a web element with the specified element_id.
        Overrides method in Selenium WebDriver in order to always give them
        Appium WebElement
        """
        self.log4py.info("创建一个id为%s的元素" %element_id)
        return self.driver.create_web_element(element_id)

    def get_app_strings(self, language=None, string_file=None):
        """Returns the application strings from the device for the specified language.
        :Args:
         - language - strings language code
         - string_file - the name of the string file to query
        """
        app_str = self.driver.app_strings
        self.log4py.info("获取app的strings" + str(app_str))
        return app_str

    def do_reset(self):
        """Resets the current application on the device.
        """
        self.driver.reset()

    def do_hide_keyboard(self, key_name=None, key=None, strategy=None):
        """Hides the software keyboard on the device. In iOS, use `key_name` to press
        a particular key, or `strategy`. In Android, no parameters are used.
        :Args:
         - key_name - key to press
         - strategy - strategy for closing the keyboard (e.g., `tapOutside`)
        """
        self.driver.hide_keyboard()

    # Needed for Selendroid
    def do_keyevent(self, keycode, metastate=None):
        """Sends a keycode to the device. Android only. Possible keycodes can be
        found in http://developer.android.com/reference/android/view/KeyEvent.html.

        :Args:
         - keycode - the keycode to be sent to the device
         - metastate - meta information about the keycode being sent
        """
        pass

    def do_press_keycode(self, keycode, metastate=None):
        """Sends a keycode to the device. Android only. Possible keycodes can be
        found in http://developer.android.com/reference/android/view/KeyEvent.html.

        :Args:
         - keycode - the keycode to be sent to the device
         - metastate - meta information about the keycode being sent
        """
        pass

    def do_long_press_keycode(self, keycode, metastate=None):
        """Sends a long press of keycode to the device. Android only. Possible keycodes can be
        found in http://developer.android.com/reference/android/view/KeyEvent.html.

        :Args:
         - keycode - the keycode to be sent to the device
         - metastate - meta information about the keycode being sent
        """
        pass

    def set_value(self, element, value):
        """Set the value on an element in the application.

        :Args:
         - element - the element whose value will be set
         - Value - the value to set on the element
        """
        self.driver.set_value(element, value)

    def do_pull_file(self, path):
        """Retrieves the file at `path`. Returns the file's content encoded as
        Base64.
        :Args:
         - path - the path to the file on the device
        """
        pass

    def do_pull_folder(self, path):
        """Retrieves a folder at `path`. Returns the folder's contents zipped
        and encoded as Base64.
        :Args:
         - path - the path to the folder on the device
        """
        pass

    def do_push_file(self, path, base64data):
        """Puts the data, encoded as Base64, in the file specified as `path`.
        :Args:
         - path - the path on the device
         - base64data - data, encoded as Base64, to be written to the file
        """
        pass

    def do_background_app(self, seconds):
        """Puts the application in the background on the device for a certain duration.
        :Args:
         - seconds - the duration for the application to remain in the background
        """
        self.driver.background_app(seconds)
        self.log4py.info("将app放置后台%s秒" %str(seconds))
        return self

    def is_app_installed(self, bundle_id):
        """Checks whether the application specified by `bundle_id` is installed
        on the device.
        :Args:
         - bundle_id - the id of the application to query
        """
        pass

    def do_install_app(self, app_path):
        """Install the application found at `app_path` on the device.
        :Args:
         - app_path - the local or remote path to the application to install
        """
        self.driver.install_app(app_path)

    def do_remove_app(self, app_id):
        """Remove the specified application from the device.

        :Args:
         - app_id - the application id to be removed
        """
        pass

    def do_launch_app(self):
        """Start on the device the application specified in the desired capabilities.
        """
        pass

    def do_close_app(self):
        """Stop the running application, specified in the desired capabilities, on
        the device.
        """
        self.driver.close_app()

    def start_activity(self, app_package, app_activity, **opts):
        """Opens an arbitrary activity during a test. If the activity belongs to
        another application, that application is started and the activity is opened.
        This is an Android-only method.
        :Args:
        - app_package - The package containing the activity to start.
        - app_activity - The activity to start.
        - app_wait_package - Begin automation after this package starts (optional).
        - app_wait_activity - Begin automation after this activity starts (optional).
        - intent_action - Intent to start (optional).
        - intent_category - Intent category to start (optional).
        - intent_flags - Flags to send to the intent (optional).
        - optional_intent_arguments - Optional arguments to the intent (optional).
        - dont_stop_app_on_reset - Should the app be stopped on reset (optional)?
        """
        return self.driver.start_activity(app_package, app_activity)

    def end_test_coverage(self, intent, path):
        """Ends the coverage collection and pull the coverage.ec file from the device.
        Android only.
        See https://github.com/appium/appium/blob/master/docs/en/android_coverage.md
        :Args:
         - intent - description of operation to be performed
         - path - path to coverage.ec file to be pulled from the device
        """
        pass

    def do_lock(self, seconds):
        """Lock the device for a certain period of time. iOS only.
        :Args:
         - the duration to lock the device, in seconds
        """
        self.driver.lock(seconds)

    def do_open_notifications(self):
        """Open notification shade in Android (API Level 18 and above)
        """
        self.driver.open_notifications()

    @property
    def do_network_connection(self):
        """Returns an integer bitmask specifying the network connection type.
        Android only.
        Possible values are available through the enumeration `appium.webdriver.ConnectionType`
        """
        return self.driver.network_connection

    def set_network_connection(self, connectionType):
        """Sets the network connection type. Android only.
        Possible values:
            Value (Alias)      | Data | Wifi | Airplane Mode
            -------------------------------------------------
            0 (None)           | 0    | 0    | 0
            1 (Airplane Mode)  | 0    | 0    | 1
            2 (Wifi only)      | 0    | 1    | 0
            4 (Data only)      | 1    | 0    | 0
            6 (All network on) | 1    | 1    | 0
        These are available through the enumeration `appium.webdriver.ConnectionType`

        :Args:
         - connectionType - a member of the enum appium.webdriver.ConnectionType
        """
        pass

    @property
    def get_available_ime_engines(self):
        """Get the available input methods for an Android device. Package and
        activity are returned (e.g., ['com.android.inputmethod.latin/.LatinIME'])
        Android only.
        """
        available_ime = self.driver.available_ime_engines
        self.log4py.info("可见的输入法：" + str(available_ime))
        return available_ime

    def is_ime_active(self):
        """Checks whether the device has IME service active. Returns True/False.
        Android only.
        """
        return self.driver.is_ime_active()

    def do_activate_ime_engine(self, engine):
        """激活输入法引擎Activates the given IME engine on the device.Android only.
        :Args:
         - engine - the package and activity of the IME engine to activate (e.g.,
            'com.android.inputmethod.latin/.LatinIME')
        """
        self.log4py.info("激活输入法引擎：" + str(engine))
        self.driver.activate_ime_engine(engine)

    def deactivate_ime_engine(self):
        """Deactivates the currently active IME engine on the device.
        Android only.
        """
        self.driver.deactivate_ime_engine()
        self.log4py.info("将当前活跃的输入法引擎失效")

    @property
    def get_active_ime_engine(self):
        """Returns the activity and package of the currently active IME engine (e.g.,
        'com.android.inputmethod.latin/.LatinIME').
        Android only.
        """
        current_ime = self.driver.active_ime_engine
        self.log4py.info("获取到当前的输入法：" + str(current_ime))
        return current_ime

    def device_time(self):
        """Returns the appium server Settings for the current session.
        Do not get Settings confused with Desired Capabilities, they are
        separate concepts. See https://github.com/appium/appium/blob/master/docs/en/advanced-concepts/settings.md
        """
        return self.driver.device_time()

    def update_settings(self, settings):
        """Set settings for the current session.
        For more on settings, see: https://github.com/appium/appium/blob/master/docs/en/advanced-concepts/settings.md

        :Args:
         - settings - dictionary of settings to apply to the current test session
        """
        pass

    def toggle_location_services(self):
        """Toggle the location services on the device. Android only.
        """
        pass

    def set_location(self, latitude, longitude, altitude):
        """Set the location of the device
        :Args:
         - latitude - String or numeric value between -90.0 and 90.00
         - longitude - String or numeric value between -180.0 and 180.0
         - altitude - String or numeric value
        """
        pass

    @property
    def get_device_time(self):
        """Returns the date and time fomr the device
        """
        return self.driver.device_time

