# AppiumTestProject

>从 2017 年后没再更新了，2022 再出发

`Appium` 自动化测试工具，比较好用的自动化工具，值得学习和研究。这个工程主要是个人对 `Appium` 结合 `Python` 在 C 端进行自动化实施上理解的一个应用方案，可通过和使用该工程进行 app 自动化测试学习和研究。
工程还在一点一点的完善，补充的内容也一点一点的在时间轴中详细描述，工程具体的流程和代码逻辑可以
自行 review，代码中有相应的注释，如有需要也可以联系我，
希望你能通过这个工程获得一些你想获取的东西。

## 对于实施 UI 自动化前的技术选型考虑角度

>不限于此

1. 脚本录制与回放
2. 脚本语言（是否支持团队技术基础上的语言）
3. 资源修改
4. 数据驱动
5. 数据驱动脚本自动转换
6. 组件自动同步
7. 模糊识别
8. 组件识别扩展
9. 动态检查（页面动态渲染）
10. 脚本扩展
11. 检查点
12. 识别组件对位置的依赖
13. 调试功能
14. 关键字驱动


## 项目依赖及环境准备

1. Python (3.7)
2. selenium (4.4.3)
3. [Appium-Python-Client (2.6.1)](https://appium.io/docs/en/about-appium/api/)

- 环境准备

1. appium (1.22.3-4)
2. miniconda ( 4.9.0)
3. adb

## 内容更新

### 2017.01.31

1.关于 appium 的通信服务如可通过代码进行开启、关闭、重启？
2.如何监控设备的链接状态？容错处理获取到的手机可用信息
3.app 版本迭代是否会影响到 Uiautomator Viewer的控件ID的获取？

### 2017.02.28

1.appium设计主链路功能UI测试的框架（数据驱动、关键字驱动）
2.实现测试过程中的性能数据收集

### 20170321

- 需求：添加 adb cmd 的api
- 项目下路径：framework/ui_test_api/adb/commond.py
- 需求概述：将adb 调试命令

### 20170329

需求：封装 appium 基础的底层api, 在整个测试用例的编写过程  
项目下路径：
需求概述：

1. 超时处理
2. 异常处理
3. 日志记录
4. 代码弱耦合
5. 逻辑强内聚
6. 减小创建的次数
7. APP监控了常用的men,cpu,fps
8. 设备重连机制
9. 邮件发送excel的测试报告
10. 支持多设备 andoird 并行

### 配置文件化-关于路径的操作

pathconfig.ini中的配置所需项的相对路径，通过 getallpath 调用 configcommonctl 来解析拿到数据数据，getallpath作为对外接口
提供最直接的操作

### 20170405

1. 第一封装层的api，不应该有超过3复杂度的设计 
2. 上层如果存在单一的逻辑直接写入底并提供调用方法

### 20170508

1. 使用 mysqldb 操作数据库
2. 使用 xlrd、xlwt和xlutils操作Excel文件

### 20170513

1. 如何进行多台设备进行同时执行？通过命令启动服务

   - 命令行参数：

       ```text
       -p: 是指定监听的端口（也可写成 --port），也可以修改为你需要的端口；

       -bp: (Android-only) 连接设备的端口号是连接Android设备bootstrap的端口号，默认是4724（也可写成--bootstrap-port）

       -U: 连接物理设备的唯一设备标识符，是连接的设备名称，如"adb devices"获取的设备标识（也可写成--udid）

       --chromedriver-port: 是chromedriver运行需要指定的端口号，默认是9515

       -a: 是指定监听的ip（也可写成 --address），后面“127.0.0.1”可以改为你需要的ip地址；

       --session-override: 是指覆盖之前的session；
       ```

   - 启动对各服务端：

       ```text
       appium -p 4492 -bp 2251 -U udid_num  
       appium -p 4493 -bp 2252 -U udid_num2  
       ......
       ```

   - 客户端多个连接：

       ```text
       在脚本的 capabilities.setCapability("udid","udid_num")   
       driver.remote("http://127.0.0.1:4492/wd/hub",cpabilities")
       udid和对应启动的服务器的端口保持一致
       端口生成、doc命令执行、获取设备列表、启动多服务器
       ```

2. 现在做的逻辑就是：获取当前连接的设备数，启动相同数量的服务器并分配好未被占用的端口，同时要确认每个设备连接的是独立的服务端口
那么脚本必须做到多线程执行，不然会报错
3. 编写实际的自动化脚本时，记得先实力化server服务，然后进行多线程的设计（待完成）

### 20170728  20170730 (计划)

获取app的启动和首页的activity，可以通过查看apk包和已安装的app

**aapt dump badging a.apk**  
**adb logcat -c && adb logcat -s ActivityManager**  

1. 启动参数配置化（run.ini）,在配置文件中读取驱动app启动的desired capabilities参数、还有关于是否重新安装的开关值
apk的安装包路径、app的启动activity、app的首页activity
2. 是否重新安装的开关值，为0时，检查是否安装，若安装了先卸载，再安装；为1时，检查是否安装，没有安装就先安装再执行后续操作
，若安装了，就直接继续后续操作
3. 根据udid来过去设备对应的port（当然多设备的时候，需要将配置文件中的内容设置为list，逗号隔开）
4. 在脚本获取appium driver时，在线程中实例化一个线程，并返回这个driver

### 20170801

1. 如果进行渠道包验证（指定目录下的所有apk，一部或多部手机，多线程数据共享） （待完成）
2. 修改command.py中的app的安装、卸载和是否安装等方法；
3. run.ini配置文件中的内容，不在进行代码设计，因为通过代码来获取app的启动activity和首页activity，没有多少现实意义，后续有时间可以考虑添加该功能；
4. 修改initappiumdriver中的数据获取方式；

### 20170802

1. APPIUM DRIVER已经设计完成，需要后续再多线程实例化和初始化上做一个详细的流程。
2. 初次启动服务并实例化driver，会出现 urllib.error.URLError，因为服务启动占用了端口，但是正式的服务内容还没有启动完成，在此时去Remote(url)就报错了，
放弃之前使用的超时、校验端口的方式，使用异常处理的方式来建立driver。
3. 同时解除InitDriverOption与ServicePort的耦合。
4. 改造InitService.generate_service_command中的数据形式，使用dict代替list。

### 20170804

1. 做了个实验，python自己的日志模块做的很好，就像自己做一下封装，当前的日志模块可以有两种实现方式：
    - 1.将所有日志等级的handler在类的__init__方法中实例化
    - 2.在类的之前以普通方式实例handler
    - 3.使用配置文件的方式设置logging，其中一个是fileconfig，一个是dictconfig
2. 第一种方法会出现同一个日志level的logger，会有个handler，也就是会重复打印n个日志内容。而第二中方法不会出现这种情况，如果想使用第一种方法，也可以，就是在
打印日志后，将当前的handler关闭并移除当前的logger.handlers[i]
3. fileconfig和dictconfig比较方便的使用，但是日志的格式无法自定义，但是可以自己进行封装。
4. 现在项目中已经demo好了四种日志模板，可以用到任意项目中。

### 20171023

1. 通过ServicePort进行初始化的服务并生成的ini配置文件中添加一个run字段，如果为0：未执行；为1：执行过
2. InitDriverOption中初始化appiumdriver时，首先读取第一步生成的配置文件如果有

### 20171027

1. 优化一下项目管理
2. 测试脚本设计的一个建议，在创建线程前，先实例化appium服务，这时候通过配置文件来获取sno和port，
随后有了唯一设备的driver，然后就去执行脚本

### 20171221

1. 优化了启动后台appium服务的逻辑，及采用了线程方式来执行启动服务的命令。
2. 多机执行将会使用multiprocessing.Pool.map_async(caseFunc, driverList)
3. 启动服务后将bootstrap对应的端口也写入配置文件中，以便关闭appium服务的时候同时关闭该端口
