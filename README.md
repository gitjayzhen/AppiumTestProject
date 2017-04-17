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
