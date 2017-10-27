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
import platform
import re
import subprocess
import sys
import time
import string
import EventKeys
import json

reload(sys)
sys.setdefaultencoding('utf8')


class AdbCmder(object):
    """
    利用可变参数来初始化*（tuple），**（dict）:约定参数中的key只能是sno
	a(1,2,3,4,4,Z=8,k=2) ： *接受k=v之前的内容，**接受k=v
    """

    def __init__(self, **serialno_num):
        self.system = None
        self.find_type = None
        self.command = "adb"
        self.__serialno_num = ""
        if "sno" in serialno_num:
            self.__serialno_num = serialno_num.get("sno")

    def get_serialno_num(self):
        return self.__serialno_num

    def set_serialno_num(self, sno):
        self.__serialno_num = sno

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
            raise EnvironmentError("Adb not found in $ANDROID_HOME path: %s." % os.environ["ANDROID_HOME"])

            # adb命令

    def adb(self, args):
        if self.__serialno_num == "" or self.__serialno_num is None:
            cmd = "%s %s" % (self.command, str(args))
        else:
            cmd = "%s -s %s %s" % (self.command, self.__serialno_num, str(args))
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def shell(self, args):
        if self.__serialno_num == "" or self.__serialno_num is None:
            cmd = "%s shell %s" % (self.command, str(args))
        else:
            cmd = "%s -s %s shell %s" % (self.command, self.__serialno_num, str(args))
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def get_device_state(self):
        """
        获取设备状态： offline | bootloader | device 等
        """
        return self.adb("get-state").stdout.read().strip()

    def get_device_sno(self):
        """
        只有一个设备，获取设备id号，return serialNo
        """
        return self.adb("get-serialno").stdout.read().strip()

    def get_device_list(self):
        devices = []
        result = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
        result.reverse()  # 将readlines结果反向排序
        for line in result[1:]:
            if "attached" not in line.strip() and "daemon" not in line.strip():
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

    def get_app_pid(self, packageName):
        """
        获取进程pid
        args:
        - packageName -: 应用包名
        usage: getPid("com.android.settings")
        """
        if self.system is "Windows":
            pidinfo = self.shell("ps | findstr %s$" % packageName).stdout.read()
        else:
            pidinfo = self.shell("ps | grep -w %s" % packageName).stdout.read()

        if pidinfo == '':
            return "the process doesn't exist."

        pattern = re.compile(r"\d+")
        result = pidinfo.split(" ")
        result.remove(result[0])

        return  pattern.findall(" ".join(result))[0]

    def get_focused_package_and_activity_2(self):
        pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
        out = self.shell("dumpsys window w | %s \/ | %s name=" % (self.find_util, self.find_util)).stdout.read()
        return pattern.findall(out)[0]

    def get_focused_package_and_activity(self):
        """
        获取当前应用界面的包名和Activity，返回的字符串格式为：packageName/activityName
        """
        return self.shell("dumpsys activity | findstr mFocusedActivity").stdout.read().split()[-2]

    def get_current_package_name(self):
        """
         获取当前运行应用的activity
         """
        return self.get_focused_package_and_activity().split("/")[0]

    def get_current_activity(self):
        """
        获取当前设备的activity
        """
        return self.get_focused_package_and_activity().split("/")[-1]

    def get_battery_level(self):
        """
        获取电池电量
        """
        level = self.shell("dumpsys battery | %s level" %self.find_type).stdout.read().split(": ")[-1]
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
        status = self.shell("dumpsys battery | %s status" %self.find_type).stdout.read().split(": ")[-1]

        return statusDict[int(status)]

    def get_battery_temp(self):
        """
        获取电池温度
        """
        temp = self.shell("dumpsys battery | %s temperature" % self.find_type).stdout.read().split(": ")[-1]
        return int(temp) / 10.0

    def get_screen_resolution(self):
        """
        获取设备屏幕分辨率，return (width, high)
        """
        pattern = re.compile(r"\d+")
        out = self.shell("dumpsys display | %s PhysicalDisplayInfo" % self.find_type).stdout.read()
        display = pattern.findall(out)

        return (int(display[0]), int(display[1]))

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
        time = self.shell("am start -W %s | %s TotalTime" % (component, self.find_type)) \
            .stdout.read().split(": ")[-1]
        return int(time)

    def do_install_app(self, appFile, pkg_name):
        """
        安装app，app名字不能含中文字符
        args:- appFile -: app路径
        usage: install("d:\\apps\\Weico.apk")
        """
        self.adb("install %s" % appFile)
        if not self.is_install_app(pkg_name):
            return True
        else:
            return False

    def do_uninstall_app(self, pkg_name):
        """
            卸载应用args:- packageName -:应用包名，非apk名
        """
        self.adb(" uninstall %s" % pkg_name)
        if not self.is_install_app(pkg_name):
            return True
        else:
            return False

    def is_install_app(self, packageName):
        """
        判断应用是否安装，已安装返回True，否则返回False
        usage: isInstall("com.example.apidemo")
        """
        flag = False
        result = self.get_third_app_list()
        if result is None or len(result) < 0:
            return None
        for i in result:
            if re.search(packageName, i.strip()):
                flag = True
        return flag

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
        packageName = self.get_current_package_name()
        component = self.get_current_activity()
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
        time.sleep(0.5)

    def do_long_press_key(self, event_keys):
        """
        发送一个按键长按事件，Android 4.4以上
        usage: longPressKey(event_keys.HOME)
        """
        self.shell("input keyevent --longpress %s" % str(event_keys))
        time.sleep(0.5)

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
        time.sleep(0.5)

    def do_touch_by_element(self, element):
        """
        点击元素
        usage: touchByElement(Element().findElementByName(u"计算器"))
        """
        self.shell("input tap %s %s" % (str(element[0]), str(element[1])))
        time.sleep(0.5)

    def do_touch_by_ratio(self, ratioWidth, ratioHigh):
        """
        通过比例发送触摸事件
        args:
        - ratioWidth -:width占比, 0<ratioWidth<1
        - ratioHigh -: high占比, 0<ratioHigh<1
        usage: touchByRatio(0.5, 0.5) 点击屏幕中心位置
        """
        self.shell("input tap %s %s" % (str(ratioWidth * self.getScreenResolution()[0]), str(ratioHigh * self.getScreenResolution()[1])))
        time.sleep(0.5)

    def do_swipe_by_coord(self, start_x, start_y, end_x, end_y, duration=" "):
        """
        滑动事件，Android 4.4以上可选duration(ms)
        usage: swipe(800, 500, 200, 500)
        """
        self.shell("input swipe %s %s %s %s %s" % (str(start_x), str(start_y), str(end_x), str(end_y), str(duration)))
        time.sleep(0.5)

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
        time.sleep(0.5)

    def do_swipe_by_ratio(self, start_ratioWidth, start_ratioHigh, end_ratioWidth, end_ratioHigh, duration=" "):
        """
        通过比例发送滑动事件，Android 4.4以上可选duration(ms)
        usage: swipeByRatio(0.9, 0.5, 0.1, 0.5) 左滑
        """
        self.shell("input swipe %s %s %s %s %s" % (str(start_ratioWidth * self.getScreenResolution()[0]), str(start_ratioHigh * self.getScreenResolution()[1]), \
                                             str(end_ratioWidth * self.getScreenResolution()[0]), str(end_ratioHigh * self.getScreenResolution()[1]), str(duration)))
        time.sleep(0.5)

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
        time.sleep(0.5)

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
                self.sendKeyEvent(EventKeys.SPACE)
        time.sleep(0.5)

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

    def do_stop_and_restart_5037(self):
        pid1 = os.popen("netstat -ano | findstr 5037 | findstr  LISTENING").read()
        if pid1 is not None:
            pid = pid1.split()[-1]
        # 下面的命令执行结果，可能因电脑而异，若获取adb.exe时出错，可自行调试！
        # E:\>tasklist /FI "PID eq 10200"
        # Image Name                     PID Session Name        Session#    Mem Usage
        # ========================= ======== ================ =========== ============
        # adb.exe                      10200 Console                    1      6,152 K

        process_name = os.popen('tasklist /FI "PID eq %s"' %pid).read().split()[-6]
        process_path = os.popen('wmic process where name="%s" get executablepath' %process_name).read().split("\r\n")[1]

        # #分割路径，得到进程所在文件夹名
        # name_list = process_path.split("\\")
        # del name_list[-1]
        # directory = "\\".join(name_list)
        # #打开进程所在文件夹
        # os.system("explorer.exe %s" %directory)
        # 杀死该进程
        os.system("taskkill /F /PID %s" %pid)
        os.system("adb start-server")

    def do_input_text(self,text):
        text_list = list(text)
        specific_symbol = set(['&','@','#','$','^','*'])
        for i in range(len(text_list)):
            if text_list[i] in specific_symbol:
                if i-1 < 0:
                    text_list.append(text_list[i])
                    text_list[0] = "\\"
                else:
                    text_list[i-1] = text_list[i-1] + "\\"
        seed = ''.join(text_list)
        self.shell('input text "%s"'%seed)

    def do_capture_window(self):
        self.shell("rm /sdcard/screenshot.png").wait()
        self.shell("/system/bin/screencap -p /sdcard/screenshot.png").wait()
        print ">>>截取屏幕成功，在桌面查看文件。"
        c_time = time.strftime("%Y_%m_%d_%H-%M-%S")
        self.adb('pull /sdcard/screenshot.png T:\\%s.png"'%c_time).wait()

    def get_srceenrecord(self,times, path):
        PATH = lambda p: os.path.abspath(p)
        sdk = string.atoi(self.shell("getprop ro.build.version.sdk").stdout.read())
        try:
            times = string.atoi(times)
        except ValueError, e:
            print ">>>Value error because you enter value is not int type, use default 'times=20s'"
            times = int(20)
        if sdk >= 19:
                self.shell("screenrecord --time-limit %d /data/local/tmp/screenrecord.mp4" % times).wait()
                print ">>>Get Video file..."
                time.sleep(1.5)
                path = PATH(path)
                if not os.path.isdir(path):
                    os.makedirs(path)
                self.adb("pull /data/local/tmp/screenrecord.mp4 %s" % PATH("%s/%s.mp4" % (path, self.timestamp()))).wait()
                self.shell("rm /data/local/tmp/screenrecord.mp4")
                print ">>>ok"
        else:
            print "sdk version is %d, less than 19!" % sdk
            sys.exit(0)

    def get_crash_log(self):
        # 获取app发生crash的时间列表
        time_list = []
        result_list = self.shell("dumpsys dropbox | findstr data_app_crash").stdout.readlines()
        for time in result_list:
            temp_list = time.split(" ")
            temp_time= []
            temp_time.append(temp_list[0])
            temp_time.append(temp_list[1])
            time_list.append(" ".join(temp_time))

        if time_list is None or len(time_list) <= 0:
            print ">>>No crash log to get"
            return None
        log_file = "T://Exception_log_%s.txt" % self.timestamp()
        f = open(log_file, "wb")
        for timel in time_list:
            cash_log = self.shell(timel).stdout.read()
            f.write(cash_log)
        f.close()
        print ">>>check local file"

    def get_permission_list(self, package_name):
        PATH = lambda p: os.path.abspath(p)
        permission_list = []
        result_list = self.shell("dumpsys package %s | findstr android.permission" %package_name).stdout.readlines()
        for permission in result_list:
            permission_list.append(permission.strip())
        pwd = os.path.join(os.getcwd(),"gui_controller\\scriptUtils")
        permission_json_file = file("%s\\permission.json"%pwd)
        file_content = json.load(permission_json_file)["PermissList"]
        name = "_".join(package_name.split("."))
        f = open(PATH("%s\\%s_permission.txt" %(pwd,name)), "w")
        f.write("package: %s\n\n" %package_name)
        for permission in permission_list:
            for permission_dict in file_content:
                if permission == permission_dict["Key"]:
                    f.write(permission_dict["Key"] + ":\n  " + permission_dict["Memo"] + "\n")
        f.close

    def timestamp(self):
        return time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))

    def get_ui_dump_xml(self, xml_path):
        """
        获取当前Activity的控件树
        """
        print xml_path
        PATH = lambda a: os.path.abspath(a)
        if int(self.get_sdk_version()) >= 19:
            self.shell("uiautomator dump --compressed /data/local/tmp/uidump.xml").wait()
        else:
            self.shell("uiautomator dump /data/local/tmp/uidump.xml").wait()
        path = PATH(xml_path)
        if not os.path.isdir(path):
            os.makedirs(path)
        self.adb("pull /data/local/tmp/uidump.xml %s" % PATH(path)).wait()
        self.shell("rm /data/local/tmp/uidump.xml").wait()
        if os.path.exists(os.path.join(path, "uidump.xml")):
            return True
        else:
            return False