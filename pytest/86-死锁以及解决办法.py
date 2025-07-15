#coding=utf-8
import threading
import time

class MyThread(threading.Thread):
    def run(self):
        if mutexA.acquire(2):
            print("thread %s is running"%threading.current_thread().name)
            time.sleep(1)
            if mutexB.acquire(2):
                print("thread %s is running"%threading.current_thread().name)
                mutexB.release()
            mutexA.release()
class MyThread2(threading.Thread):
    def run(self):
        if mutexB.acquire(2):
            print("thread %s is running"%threading.current_thread().name)
            time.sleep(1)
            if mutexA.acquire(2):
                print("thread %s is running"%threading.current_thread().name)
                mutexA.release()
            mutexB.release()

mutexA = threading.Lock()
mutexB = threading.Lock()

if __name__ == "__main__":
    t1 = MyThread()
    t2 = MyThread2()
    t1.start()
    t2.start()
    t1.join()
    t2.join()