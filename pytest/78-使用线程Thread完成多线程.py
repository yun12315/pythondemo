import time
from threading import Thread


#1.如果多个线程执行的都是同一个函数的话，那么线程之间是并发执行的。
def test():
    print("----test----")
    time.sleep(1)

for i in range(5):
     t = Thread(target=test) #同一进程里创建多个线程
     t.start()
    #test()