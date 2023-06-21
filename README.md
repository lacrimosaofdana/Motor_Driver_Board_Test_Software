# 季丰电机驱动板测试软件

## 环境

Python 3.11 and MySQL 8.0


## 安装

Load the sql file

```
$ /usr/local/MySQL/bin/mysql -u root -p
Enter password:
mysql> source cs4400_database_v2 schema_and_data.sql
mysql> source cs4400_phase3_stored_procedures_team#78.sql
```

Modify the app.py

```
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysqs://username:password@127.0.0.1:3306/database_name'
```

Please notice that the username, password and database_name is your own setting of database.

create & active virtual enviroment then install all the required packages of Python:

```
$ python3 -m venv venv
$ source venv/bin/activate 
(env) $ pip install -r requirements.txt
```

Run the program:

```
(env) $ flask run
* Running on http://127.0.0.1:5000/
```

## Explanation

Front-end is based on the bootstrap template. For the back end, we implement it by flask, which is a micro web framework written in Python.



