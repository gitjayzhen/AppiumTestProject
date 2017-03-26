#-*- coding=utf-8 -*-
import os
import re
import datetime
import time
from deviceinfoctl import DeviceController
from com.framework.core.adb.commond import AdbCmder
'''
主要处理安装和卸载手机上的应用
'''
class PackageController():
    def __init__(self):
        self.sno_list = DeviceController().get_devices()
        self.android = AdbCmder()
    '''
    uninstall_All参数指定要卸载的包名，该方法会调用uninstall_One卸载所有链接在电脑上的手机中的应用
    '''
    def uninstall_all(self,package_name):
        devices = self.sno_list
        if devices is None:
            print ">>>No device is connected"
        else:
            for sno in devices:
                uninstall_one(sno,package_name)
    '''
    指定设备，并指定包名进行应用的卸载
    '''
    def uninstall_one(self,sno,package_name):
        uninstall_result = self.android.adb(sno,'uninstall %s'%package_name).stdout.read()
        if re.findall(r'Success',uninstall_result):
            print '>>>[%s] uninstall [%s] [SUCCESS]' %(sno,package_name)
        else:
            print '>>>no assign package'
    '''
    apk_name为apk的绝对路径，该方法会调用install_OneDevice方法，向所有设备安装该应用
    '''
    def install_all_devices(self,apk_name,apk_package_name):
        print ">>>Install all devices"
        device_list = self.sno_list
        if device_list is None:
            print ">>>No device is connected"
        else:
            for sno in device_list:
                self.install_one_device(sno,apk_name,apk_package_name)

    '''
    指定设备名，并指定apk进行安装，安装前会检测手机是否已经安装了该应用，如果有，先卸载
    '''
    def install_one_device(self,sno,apk_name,apk_package_name):
        had_package = self.android.shell(sno,'pm list packages |findstr "%s"'%apk_package_name).stdout.read()
        if re.search(apk_package_name,had_package):
            self.uninstall_one(sno,apk_package_name)
        install_result = self.android.adb(sno,'install %s'%apk_name).stdout.read()
        boolean = self.is_has_package(sno,apk_package_name)
        if re.findall(r'Success',install_result) or boolean:
            print '>>>[%s] adb install %s [SUCCESS]' %(sno,os.path.basename(apk_name))
        else:
            print '>>>[%s] install %s [FALSE]'%(sno,os.path.basename(apk_name))

    def cover_install(self,sno,apk_name,apk_package_name):
        install_result = self.android.adb(sno,'install -r %s'%apk_name).stdout.read()
        boolean = self.is_has_package(sno,apk_package_name)
        if re.findall(r'Success',install_result) or boolean:
            print '>>>[%s] adb install %s [SUCCESS]' %(sno,os.path.basename(apk_name))
        else:
            print '>>>[%s] install %s [FALSE]'%(sno,os.path.basename(apk_name))

    def is_has_package(self,sno,package_name):
        had_package = self.android.shell(sno,'pm list packages |findstr "%s"'%package_name).stdout.read()
        if re.search(package_name,had_package):
            return True
        else:
            return False

    def clear_app_data(self,sno,package_name):
        b = self.is_has_package(sno, package_name)
        if b:
            res = self.android.shell(sno,"pm clear %s"%package_name).stdout.read()
            if re.search(r'Success',res):
                print ">>> Clear data Success with [%s]"%package_name
            else:
                print ">>> Clear work ERROR"
        else:
            print ">>> NO Package :",package_name


