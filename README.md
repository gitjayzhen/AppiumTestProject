# AppiumTestProject
Appium自动化测试工具，比较好用的自动化工具，你值得学习。


#20170321
需求：添加adb cmd的api
项目下路径：/src/com/framework/ui_test_api/adb/commond.py
需求概述：将adb 调试命令

#20170339
需求：封装appium基础的底层api
项目下路径：
需求概述：<br>
    1.超时处理<br>
    2.异常处理<br>
    3.日志记录<br>
    4.弱耦合<br>
    5.强内聚<br>
    6.减小创建的次数<br>

#配置文件化-关于路径的操作
pathconfig.ini中的配置所需项的相对路径，通过getallpath调用configcommonctl来解析拿到数据数据，getallpath作为对外接口
提供最直接的操作

#20170405
1.第一封装层的api，不应该有超过3复杂度的设计<br>
2.上层如果存在单一的逻辑直接写入底并提供调用方法

#20170508
1.使用mysqldb操作数据库<br>
2.使用xlrd、xlwt和xlutils操作Excel文件

#20170513
1.如何进行多台设备进行同时执行<br>
                -p：监听端口    -bp：连接设备的端口号   -U:连接物理设备的唯一设备标识符<br>
    启动对各服务端：appium -p 4492 -bp 2251 -U udid_num<br>
                 appium -p 4493 -bp 2252 -U udid_num2<br>
                 ......<br>
    客户端多个连接：在脚本的capabilities.setCapability("udid","udid_num")<br>
                 driver.remote("http://127.0.0.1:4492/wd/hub",cpabilities<br>
                 udid和对应启动的服务器的端口保持一致<br>
    <p>端口生成、doc命令执行、获取设备列表、启动多服务器</p>
    
2.现在做的逻辑就是：获取当前连接的设备数，启动相同数量的服务器并分配好未被占用的端口，同时要确认每个设备连接的是独立的服务端口
那么脚本必须做到多线程执行，不然会报错

