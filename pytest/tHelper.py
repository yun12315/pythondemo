# -*- coding: utf-8 -*-

from MysqlHelper import MysqlHelper

db = MysqlHelper("192.168.0.254", 3306, "root", "kingdee@123", "shop_neands")

# 插入数据
# name = input("请输入姓名:")
# sid = input("请输入学号:")
# name = name.encode("utf-8").decode("gbk")
# sql = 'insert into test(name,sid) values(%s,%s)'
# params = (name, sid)
# db.cud(sql, params)

# 查询数据
parmeter = input("请按回车键查询数据:")
sql = 'select * from test where sid=%s'
result = db.find_all(sql,parmeter)
for row in result:
    print(row)