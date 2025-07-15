#coding=utf-8
import threading
import time

class MyThread(threading.Thread):
    def run(self):
        for i in range(5):
            print('%s is running' % threading.current_thread().name)
            time.sleep(1)
            msg = 'I am %s' + self.name+ '@' + str(i) # 创建一个线程，并指定线程的名字,name 属性就是线程的名字
            print(msg)
            print(msg)

if __name__ == '__main__':
    t = MyThread()
    t.start()