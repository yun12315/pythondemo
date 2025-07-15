from threading import Thread, Lock
import time

g_num = 0
g_flag = 1

def test1():
    global g_num
    global g_flag
    #这个线程和test2线程是互斥的，互斥锁，同一时刻只能有一个线程持有锁
    #mutex.acquire()
    #if g_flag == 1:
    for i in range(1000000):
        mutex.acquire()
        g_num += 1
        mutex.release() #释放锁，才能让test2线程执行
    #mutex.release()
    #g_flag = 0
    print("------test1----g_num=%d"%g_num)

def test2():
    global g_num
    #mutex.acquire()
    #while True:
        #if g_flag != 1:
    for i in range(1000000):
        mutex.acquire()
        g_num += 1
        mutex.release()
    #mutex.release()
    #break
    print("---test2---g_num=%d"%g_num)

#创建一把互斥锁，这个锁默认是没有上锁的
mutex = Lock()

p1 = Thread(target=test1)
p1.start()

p2 = Thread(target=test2)
p2.start()

print("----g_num=%d"%g_num)