from threading import Thread
import threading
import time

# 线程函数, 线程函数中不能修改全局变量
def test1():
    name = threading.current_thread().name
    print("---in test1---name=%s"%name)
    g_num = 100
    if name == "Thread-1 (test1)":
        g_num += 1
    else:
        time.sleep(2)
    print("---in test1 g_num=%d---"%g_num)
    #time.sleep(2)
    #print("---test1---g_num=%d"%g_num)

# def test2():
#     time.sleep(1)
#     g_num = 100
#     print("---in test2---g_num=%d"%g_num)

p1 = Thread(target=test1)
p1.start()

p2 = Thread(target=test1)
p2.start()