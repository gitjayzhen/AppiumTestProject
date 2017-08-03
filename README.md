# AppiumTestProject
<p> &nbsp; &nbsp; &nbsp; &nbsp;Appium自动化测试工具，比较好用的自动化工具，你值得学习。这个工程主要是个人对appium和Python理解的一个应用，可使用该工程进行app自动化测试。
工程还在一点一点的完善，补充的内容也一点一点的在时间轴中详细描述，工程具体的流程和代码逻辑可以自行review，代码中有相应的注释，如有需要也可以联系我 （邮箱：jayzhen_testing@163.com） ，希望你能通过这个工程获得一些你想获取的东西。
</P>


## 工程依赖及版本号：
1. node (6.10.2)<br>
2. appium (1.4.16)<br>
3. Python (2.7.13)<br>
4. selenium (3.4.1)<br>
5. Appium-Python-Client (0.24)<br>


# 时间轴
## 20170321
- 需求：添加adb cmd的api<br>
- 项目下路径：/src/com/framework/ui_test_api/adb/commond.py<br>
- 需求概述：将adb 调试命令<br>


## 20170329
需求：封装appium基础的底层api, 在整个测试用例的编写过程，<br>
项目下路径：<br>
需求概述：<br>
1. 超时处理<br>
2. 异常处理<br>
3. 日志记录<br>
4. 代码弱耦合<br>
5. 逻辑强内聚<br>
6. 减小创建的次数<br>


### 配置文件化-关于路径的操作
pathconfig.ini中的配置所需项的相对路径，通过getallpath调用configcommonctl来解析拿到数据数据，getallpath作为对外接口
提供最直接的操作


## 20170405
1. 第一封装层的api，不应该有超过3复杂度的设计<br>
2. 上层如果存在单一的逻辑直接写入底并提供调用方法


## 20170508
1. 使用mysqldb操作数据库<br>
2. 使用xlrd、xlwt和xlutils操作Excel文件


## 20170513
1. 如何进行多台设备进行同时执行？通过命令启动服务<br>
    命令行参数：
    >-p：监听端口  
    -bp：(Android-only) 连接设备的端口号  
    -U: 连接物理设备的唯一设备标识符  
    
    启动对各服务端：
    >appium -p 4492 -bp 2251 -U udid_num  
    appium -p 4493 -bp 2252 -U udid_num2  
    ......

    客户端多个连接：
    >在脚本的capabilities.setCapability("udid","udid_num")
    driver.remote("http://127.0.0.1:4492/wd/hub",cpabilities")
    udid和对应启动的服务器的端口保持一致<br>
    端口生成、doc命令执行、获取设备列表、启动多服务器
    
2. 现在做的逻辑就是：获取当前连接的设备数，启动相同数量的服务器并分配好未被占用的端口，同时要确认每个设备连接的是独立的服务端口
那么脚本必须做到多线程执行，不然会报错


## 20170728  20170730 (计划)
获取app的启动和首页的activity，可以通过查看apk包和已安装的app<br>
** aapt dump badging a.apk **
** adb logcat -c && adb logcat -s ActivityManager **<br><br>
1. 启动参数配置化（run.ini）,在配置文件中读取驱动app启动的desired capabilities参数、还有关于是否重新安装的开关值
apk的安装包路径、app的启动activity、app的首页activity<br><br>
2. 是否重新安装的开关值，为0时，检查是否安装，若安装了先卸载，再安装；为1时，检查是否安装，没有安装就先安装再执行后续操作
，若安装了，就直接继续后续操作<br><br>
3. 根据udid来过去设备对应的port（当然多设备的时候，需要将配置文件中的内容设置为list，逗号隔开）<br><br>
4. 在脚本获取appium driver时，在线程中实例化一个线程，并返回这个driver<br><br>


## 20170801
1. 如果进行渠道包验证（指定目录下的所有apk，一部或多部手机，多线程数据共享） （待完成）<br>
2. 修改command.py中的app的安装、卸载和是否安装等方法；<br>
3. run.ini配置文件中的内容，不在进行代码设计，因为通过代码来获取app的启动activity和首页activity，没有多少现实意义，后续有时间可以考虑添加该功能；
4. 修改initappiumdriver中的数据获取方式；

## 20170802
1. APPIUM DRIVER已经设计完成，需要后续再多线程实例化和初始化上做一个详细的流程

## 20170710  待完成
1. demo一个短信生成器
2. demo一个联系人生成器（联系人的存储形式要不同）
