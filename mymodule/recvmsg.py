# -*- coding: utf-8 -*-
import socket
import db
import pymysql

def recvmsg(sock, size):
    """
    接收消息
    :param sock: socket 对象
    :param size: 接收的消息大小
    :return: 接收到的数据
    """
    # 假设需要使用数据库连接
    try:
        name = input("请输入用户名:")

        db_connection = pymysql.connect(
            user="root",
            password="kingdee@123",
            host ="192.168.0.254",
            port=3306,
            database="shop_neands",
            charset="utf8mb4"
        )
        # 使用数据库连接进行操作
        cursor = db_connection.cursor()
        count = cursor.execute("SELECT * FROM shop_store")

        # sid = input("请输入id:")
        # sid = int(sid)
        # sql = 'update shop_store set ad_org_id=%s where id=137130'
        # cursor.execute(sql, sid)
        name = name.encode('utf-8').decode('utf-8')
        sql1 = 'insert into test(name) values(%s)'
        cursor.execute(sql1, [name])

        db_connection.commit()
        print(count)
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        # 关闭数据库连接
        cursor.close()
        db_connection.close()

    except AttributeError as e:
        print(f"数据库连接失败: {e}")
        return None


    # sock.connect(("192.168.0.254", 3306))
    # data = b''
    # while len(data) < size:
    #     d = sock.recv(size - len(data))
    #     if not d:
    #         return None
    #     data += d
    #     sock.sendall(data)
    # return data

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = recvmsg(sock, 1024)
    print(data)
