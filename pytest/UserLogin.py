# -*- coding: utf-8 -*-
from importlib import reload

from MysqlHelper import MysqlHelper
from hashlib import sha1
import sys
reload(sys)

# 用户登录
name = input("请输入用户名：")
password = input("请输入密码：")
# 加密
password = sha1(password.encode('utf-8')).hexdigest()
#print(password)
#print(sys.path)
# 连接数据库
mysql = MysqlHelper("192.168.0.254", 3306, "root", "kingdee@123", "mysql")
sql = 'select truename,passwdhash from shop_users where truename=%s'
result = mysql.find_all(sql, [name])
if result:
    if result[0][0] == password:
        print("登录成功")
    else:
        print("密码错误")
else:
    print("用户名不存在")

print(result)