#!/usr/bin/env python
# coding=utf-8

import os
import sys
import platform
import subprocess
import re
from time import sleep
from com.framework.core.appiumdriver import eventkeys

reload(sys)
sys.setdefaultencoding('utf8')

class AdbCmder(object):
    def __init__(self):
        self.system = None
        self.find_type = None
        self.command = "adb"

    def judgment_system_type(self):
        # 判断系统类型，windows使用findstr，linux使用grep
        self.system = platform.system()
        if self.system is "Windows":
            self.find_type = "findstr"
        else:
            self.find_type = "grep"

    def judgment_system_environment_variables(self):
        self.judgment_system_type()
        # 判断是否设置环境变量ANDROID_HOME
        if "ANDROID_HOME" in os.environ:
            if self.system == "Windows":
                self.command = "adb"  # os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb.exe")
            else:
                self.command = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb")
        else:
            raise EnvironmentError(
                "Adb not found in $ANDROID_HOME path: %s." % os.environ["ANDROID_HOME"])

            # adb命令

    def adb(self, serialno_num, args):
        cmd = "%s -s %s %s" % (self.command, serialno_num, str(args))
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


        # adb shell命令
    def shell(self, serialno_num, args):
        cmd = "%s -s %s shell %s" % (self.command, serialno_num, str(args))
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def get_device_state(self):
        """
        获取设备状态： offline | bootloader | device 等
        """
        return self.adb("get-state").stdout.read().strip()

    def get_device_sno(self):
        """
        获取设备id号，return serialNo
        """
        return self.adb("get-serialno").stdout.read().strip()

    def get_device_list(self):
        devices = []
        result = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
        result.reverse()  #将readlines结果反向排序
        for line in result[1:]:
            if "attached" not in line.strip():
                devices.append(line.split()[0])
            else:
                break
        return devices

    def get_android_os_version(self):
        """
        获取设备中的Android版本号，如4.2.2
        """
        return self.shell("getprop ro.build.version.release").stdout.read().strip()

    def get_sdk_version(self):
        """
        获取设备SDK版本号
        """
        return self.shell("getprop ro.build.version.sdk").stdout.read().strip()

    def get_device_model(self):
        """
        获取设备型号
        """
        return self.shell("getprop ro.product.model").stdout.read().strip()

    def get_process_id(self, packageName):
        """
        获取进程pid
        args:
        - packageName -: 应用包名
        usage: getPid("com.android.settings")
        """
        if system is "Windows":
            pidinfo = self.shell("ps | findstr %s$" % packageName).stdout.read()
        else:
            pidinfo = self.shell("ps | grep -w %s" % packageName).stdout.read()

        if pidinfo == '':
            return "the process doesn't exist."

        pattern = re.compile(r"\d+")
        result = pidinfo.split(" ")
        result.remove(result[0])

        return  pattern.findall(" ".join(result))[0]

    def do_kill_process(self, pid):
        """
        杀死应用进程
        args:
        - pid -: 进程pid值
        usage: killProcess(154)
        注：杀死系统应用进程需要root权限
        """
        if self.shell("kill %s" % str(pid)).stdout.read().split(": ")[-1] == "":
            return "kill success"
        else:
            return self.shell("kill %s" % str(pid)).stdout.read().split(": ")[-1]

    def do_quit_app(self, packageName):
        """
        退出app，类似于kill掉进程
        usage: quitApp("com.android.settings")
        """
        self.shell("am force-stop %s" % packageName)

    def get_focused_package_and_activity_2(self):
        pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
        out = self.shell("dumpsys window w | %s \/ | %s name=" % (find_util, find_util)).stdout.read()
        return pattern.findall(out)[0]

    def get_focused_package_and_activity(self,sno):
        """
        获取当前应用界面的包名和Activity，返回的字符串格式为：packageName/activityName
        """
        return self.shell(sno,"dumpsys activity | findstr mFocusedActivity").stdout.read().split()[-2]

    def get_current_package_name(self, sno):
        """
         获取当前运行应用的activity
         """
        return self.get_focused_package_and_activity(sno).split("/")[0]

    def get_current_activity(self,sno):
        """
        获取当前设备的activity
        """
        return self.get_focused_package_and_activity(sno).split("/")[-1]

    def get_battery_level(self):
        """
        获取电池电量
        """
        level = self.shell("dumpsys battery | %s level" % find_util).stdout.read().split(": ")[-1]

        return int(level)

    def get_battery_status(self):
        """
        获取电池充电状态
        BATTERY_STATUS_UNKNOWN：未知状态
        BATTERY_STATUS_CHARGING: 充电状态
        BATTERY_STATUS_DISCHARGING: 放电状态
        BATTERY_STATUS_NOT_CHARGING：未充电
        BATTERY_STATUS_FULL: 充电已满
        """
        statusDict = {1 : "BATTERY_STATUS_UNKNOWN",
                      2 : "BATTERY_STATUS_CHARGING",
                      3 : "BATTERY_STATUS_DISCHARGING",
                      4 : "BATTERY_STATUS_NOT_CHARGING",
                      5 : "BATTERY_STATUS_FULL"}
        status = self.shell("dumpsys battery | %s status" % find_util).stdout.read().split(": ")[-1]

        return statusDict[int(status)]

    def get_battery_temp(self):
        """
        获取电池温度
        """
        temp = self.shell("dumpsys battery | %s temperature" % find_util).stdout.read().split(": ")[-1]

        return int(temp) / 10.0

    def get_screen_resolution(self):
        """
        获取设备屏幕分辨率，return (width, high)
        """
        pattern = re.compile(r"\d+")
        out = self.shell("dumpsys display | %s PhysicalDisplayInfo" % find_util).stdout.read()
        display = pattern.findall(out)

        return (int(display[0]), int(display[1]))

    def do_reboot(self):
        """
        重启设备
        """
        self.adb("reboot")

    def do_fastboot(self):
        """
        进入fastboot模式
        """
        self.adb("reboot bootloader")

    def get_system_app_list(self):
        """
        获取设备中安装的系统应用包名列表
        """
        sysApp = []
        for packages in self.shell("pm list packages -s").stdout.readlines():
            sysApp.append(packages.split(":")[-1].splitlines()[0])

        return sysApp

    def get_third_app_list(self):
        """
        获取设备中安装的第三方应用包名列表
        """
        thirdApp = []
        for packages in self.shell("pm list packages -3").stdout.readlines():
            thirdApp.append(packages.split(":")[-1].splitlines()[0])

        return thirdApp

    def get_matching_app_list(self, keyword):
        """
        模糊查询与keyword匹配的应用包名列表
        usage: getMatchingAppList("qq")
        """
        matApp = []
        for packages in self.shell("pm list packages %s" % keyword).stdout.readlines():
            matApp.append(packages.split(":")[-1].splitlines()[0])

        return matApp

    def get_app_start_total_time(self, component):
        """
        获取启动应用所花时间
        usage: getAppStartTotalTime("com.android.settings/.Settings")
        """
        time = self.shell("am start -W %s | %s TotalTime" % (component, find_util)) \
            .stdout.read().split(": ")[-1]
        return int(time)

    def do_install_app(self, appFile):
        """
        安装app，app名字不能含中文字符
        args:
        - appFile -: app路径
        usage: install("d:\\apps\\Weico.apk")
        """
        self.adb("install %s" % appFile)

    def is_install_app(self, packageName):
        """
        判断应用是否安装，已安装返回True，否则返回False
        usage: isInstall("com.example.apidemo")
        """
        if self.getMatchingAppList(packageName):
            return True
        else:
            return False

    def do_remove_app(self, packageName):
        """
        卸载应用
        args:
        - packageName -:应用包名，非apk名
        """
        self.adb("uninstall %s" % packageName)

    def do_clear_app_data(self, packageName):
        """
        清除应用用户数据
        usage: clearAppData("com.android.contacts")
        """
        if "Success" in self.shell("pm clear %s" % packageName).stdout.read().splitlines():
            return "clear user data success "
        else:
            return "make sure package exist"

    def do_reset_current_app(self):
        """
        重置当前应用
        """
        packageName = self.getCurrentPackageName()
        component = self.getFocusedPackageAndActivity()
        self.do_clear_app_data(packageName)
        self.do_start_activity(component)

    def do_start_activity(self, component):
        """
        启动一个Activity
        usage: startActivity(component = "com.android.settinrs/.Settings")
        """
        self.shell("am start -n %s" % component)

    def do_start_webpage(self, url):
        """
        使用系统默认浏览器打开一个网页
        usage: startWebpage("http://www.baidu.com")
        """
        self.shell("am start -a android.intent.action.VIEW -d %s" % url)

    def do_call_phone(self, number):
        """
        启动拨号器拨打电话
        usage: callPhone(10086)
        """
        self.shell("am start -a android.intent.action.CALL -d tel:%s" % str(number))

    def do_send_key_event(self, event_keys):
        """
        发送一个按键事件
        args:
        - event_keys -:
        http://developer.android.com/reference/android/view/KeyEvent.html
        usage: sendKeyEvent(event_keys.HOME)
        """
        self.shell("input keyevent %s" % str(event_keys))
        sleep(0.5)

    def do_long_press_key(self, event_keys):
        """
        发送一个按键长按事件，Android 4.4以上
        usage: longPressKey(event_keys.HOME)
        """
        self.shell("input keyevent --longpress %s" % str(event_keys))
        sleep(0.5)

    def do_touch(self, e=None, x=None, y=None):
        """
        触摸事件
        usage: touch(e), touch(x=0.5,y=0.5)
        """
        if(e != None):
            x = e[0]
            y = e[1]
        if(0 < x < 1):
            x = x * self.width
        if(0 < y < 1):
            y = y * self.high

        self.shell("input tap %s %s" % (str(x), str(y)))
        sleep(0.5)

    def do_touch_by_element(self, element):
        """
        点击元素
        usage: touchByElement(Element().findElementByName(u"计算器"))
        """
        self.shell("input tap %s %s" % (str(element[0]), str(element[1])))
        sleep(0.5)

    def do_touch_by_ratio(self, ratioWidth, ratioHigh):
        """
        通过比例发送触摸事件
        args:
        - ratioWidth -:width占比, 0<ratioWidth<1
        - ratioHigh -: high占比, 0<ratioHigh<1
        usage: touchByRatio(0.5, 0.5) 点击屏幕中心位置
        """
        self.shell("input tap %s %s" % (str(ratioWidth * self.getScreenResolution()[0]), str(ratioHigh * self.getScreenResolution()[1])))
        sleep(0.5)

    def do_swipe_by_coord(self, start_x, start_y, end_x, end_y, duration=" "):
        """
        滑动事件，Android 4.4以上可选duration(ms)
        usage: swipe(800, 500, 200, 500)
        """
        self.shell("input swipe %s %s %s %s %s" % (str(start_x), str(start_y), str(end_x), str(end_y), str(duration)))
        sleep(0.5)

    def do_swipe(self, e1=None, e2=None, start_x=None, start_y=None, end_x=None, end_y=None, duration=" "):
        """
        滑动事件，Android 4.4以上可选duration(ms)
        usage: swipe(e1, e2)
               swipe(e1, end_x=200, end_y=500)
               swipe(start_x=0.5, start_y=0.5, e2)
        """
        if(e1 != None):
            start_x = e1[0]
            start_y = e1[1]
        if(e2 != None):
            end_x = e2[0]
            end_y = e2[1]
        if(0 < start_x < 1):
            start_x = start_x * self.width
        if(0 < start_y < 1):
            start_y = start_y * self.high
        if(0 < end_x < 1):
            end_x = end_x * self.width
        if(0 < end_y < 1):
            end_y = end_y * self.high

        self.shell("input swipe %s %s %s %s %s" % (str(start_x), str(start_y), str(end_x), str(end_y), str(duration)))
        sleep(0.5)

    def do_swipe_by_ratio(self, start_ratioWidth, start_ratioHigh, end_ratioWidth, end_ratioHigh, duration=" "):
        """
        通过比例发送滑动事件，Android 4.4以上可选duration(ms)
        usage: swipeByRatio(0.9, 0.5, 0.1, 0.5) 左滑
        """
        self.shell("input swipe %s %s %s %s %s" % (str(start_ratioWidth * self.getScreenResolution()[0]), str(start_ratioHigh * self.getScreenResolution()[1]), \
                                             str(end_ratioWidth * self.getScreenResolution()[0]), str(end_ratioHigh * self.getScreenResolution()[1]), str(duration)))
        sleep(0.5)

    def do_swipe_to_left(self):
        """
        左滑屏幕
        """
        self.swipeByRatio(0.8, 0.5, 0.2, 0.5)

    def do_swipe_to_right(self):
        """
        右滑屏幕
        """
        self.swipeByRatio(0.2, 0.5, 0.8, 0.5)

    def do_swipe_to_up(self):
        """
        上滑屏幕
        """
        self.swipeByRatio(0.5, 0.8, 0.5, 0.2)

    def do_swipe_to_down(self):
        """
        下滑屏幕
        """
        self.swipeByRatio(0.5, 0.2, 0.5, 0.8)

    def do_long_press(self, e=None, x=None, y=None):
        """
        长按屏幕的某个坐标位置, Android 4.4
        usage: longPress(e)
               longPress(x=0.5, y=0.5)
        """
        self.swipe(e1=e, e2=e, start_x=x, start_y=y, end_x=x, end_y=y, duration=2000)

    def do_long_press_element(self, e):
        """
       长按元素, Android 4.4
        """
        self.shell("input swipe %s %s %s %s %s" % (str(e[0]), str(e[1]), str(e[0]), str(e[1]), str(2000)))
        sleep(0.5)

    def do_long_press_by_ratio(self, ratioWidth, ratioHigh):
        """
        通过比例长按屏幕某个位置, Android.4.4
        usage: longPressByRatio(0.5, 0.5) 长按屏幕中心位置
        """
        self.swipeByRatio(ratioWidth, ratioHigh, ratioWidth, ratioHigh, duration=2000)

    def do_send_text(self, string):
        """
        发送一段文本，只能包含英文字符和空格，多个空格视为一个空格
        usage: sendText("i am unique")
        """
        text = str(string).split(" ")
        out = []
        for i in text:
            if i != "":
                out.append(i)
        length = len(out)
        for i in xrange(length):
            self.shell("input text %s" % out[i])
            if i != length - 1:
                self.sendKeyEvent(event_keys.SPACE)
        sleep(0.5)


