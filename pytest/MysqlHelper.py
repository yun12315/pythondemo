# -*- coding: utf-8 -*-
from pymysql import *

class MysqlHelper:
    def __init__(self,host,port,user,password,dbname,charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.charset = charset
    def connect(self):
        try:
            self.conn = connect(host=self.host,port=self.port,user=self.user,password=self.password,db=self.dbname,charset=self.charset)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"连接数据库失败：{e}")

    def cud(self,sql,params=[]):
        self.connect()
        try:
            self.cursor.execute(sql,params)
            self.conn.commit()
            print(f"执行成功！影响的行数："+str(self.cursor.rowcount))
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.close()
    def find_all(self,sql,params=[]):
        self.connect() #  <--- Changed this line
        try:
            self.cursor.execute(sql,params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"执行SQL失败：{e}")
            return None
        finally:
            self.close()
    def find_one(self,sql,params=[]):
        self.connect() #  <--- Changed this line
        try:
            self.cursor.execute(sql,params)
            return self.cursor.fetchone()
        except Exception as e:
            print(f"执行SQL失败：{e}")
            return None
        finally:
            self.close()

    def close(self):
        if hasattr(self,'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self,'conn') and self.conn:
            self.conn.close()
