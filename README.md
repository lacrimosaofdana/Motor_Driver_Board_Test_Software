# 季丰电机驱动板测试软件

## 环境

Python 3.11 and MySQL 8.0

## 系统

MacOS 13.3

## 安装

以下安装流程皆为命令行操作

首先进入MySQL Server的bin目录下，然后输入命令和密码, macos一般在/usr/local/mysql/bin下，windows找到对应bin目录操作相同

```
$ mysql -u root -p
Enter password:
```

然后将sql文件放入目录，或者进入sql所在目录下加载sql文件，创建数据库

`mysql> source test_schema.sql`

修改__init__.py文件

```
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysqs://username:password@127.0.0.1:3306/database_name'
```

请确保用户名username，密码password和数据库名database_name修改为你自己的值。

首先确保您进入了当前项目的目录，然后创建并激活当前的虚拟python环境，安装所有需求的python包。

```
$ python3 -m venv venv
$ source venv/bin/activate 
(venv) $ pip install -r requirements.txt
```

运行程序:

```
(venv) $ flask run
* Running on http://127.0.0.1:5000/
```

如有需求，可以重新生成requirements.txt文件来保存项目所需要的包，如果已存在requirements.txt，可以在指令后添加--force

安装

`pip install pipreqs`

用法

`pipreqs /home/project/location (--force)`

或者

`pipreqs . (--force)`

## 项目描述

本项目基于Python，采用B/S软件架构，数据库使用MySQL，测试通信协议采用MODBUS协议。

之前电机驱动板的测试软件关于电压测试，电流测试，功率测试，转速测试因为采用的电流表、电压表，转速表不支持串口（MODBUS）的控制和数据读取功能，因此不能把测试结果上传到MES系统中，对测试数据和测试结果进行管控，不利于产品质量的提高。因此需要对测试工装重新设计，采用具有串口（MODBUS）功能的测试表，新开发对应的测试软件，利用测试软件进行控制测试和读取测试结果，数据上传到MES。



