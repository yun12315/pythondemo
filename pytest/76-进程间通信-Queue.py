# coding=utf-8
from multiprocessing import Queue, Process, Manager, Pool
import os,time,random

# q = Queue(3)
# print(q.qsize())
# q.put('a')
# print(q.qsize())
# q.put('b')
# print(q.qsize())
# q.put('c')
# print(q.qsize())
# print(q.get())
# print(q.get())
# print(q.get())
#
# if q.empty():
#     print('empty')
# else:
#     print('not empty')
#
# if q.full():
#     print('full')
# else:
#     print('not full')

# 写数据进程执行的代码：
# def write(q):
#     print('Process to write: %s' % os.getpid())
#     for value in ['A', 'B', 'C']:
#         print('Put %s to queue...' % value)
#         q.put(value)
#         time.sleep(random.random())
#
# # 读数据进程执行的代码：
# def read(q):
#     print('Process to read: %s' % os.getpid())
#     while True:
#         if not q.empty():
#             value = q.get(True)
#             print('Get %s from queue.' % value)
#         else:
#             break

# if __name__=='__main__':
#     # 父进程创建Queue，并传给各个子进程：
#     q = Queue()
#     pw = Process(target=write, args=(q,))
#     pr = Process(target=read, args=(q,))
#     # 启动子进程pw，写入:
#     pw.start()
#     # 等待pw结束:
#     pw.join()
#     # 启动子进程pr，读取:
#     pr.start()
#     pr.join()
#     print('All done.')
#     print(q.qsize())
#     print(q.get())
#     # pr进程里是死循环，无法等待其结束，只能强行终止:
#     #pr.terminate()
#     #pw.close()
#     #pr.close()

def reader(q):
    print("reader启动(%s),父进程为(%s)"%(os.getpid(),os.getppid()))
    for i in range(q.qsize()):
        print("reader从Queue获取到消息: %s"%q.get(True))

def writer(q):
    print("writer启动(%s),父进程为(%s)"%(os.getpid(),os.getppid()))
    for i in "ABC":
        print("writer puts %s to queue."%i)
        q.put(i)

if __name__=="__main__":
    print("(%s) start"%os.getpid())
    q = Manager().Queue() # 创建一个Queue，父进程向Queue中写入数据，子进程从Queue中读取数据。
    po = Pool()
    # 使用阻塞模式创建进程，这样就不需要在reader中使用死循环了，可以让writer完全执行完成后，再用reader,创建两个子进程，一个负责写入，一个负责读取
    po.apply(writer,(q,))
    po.apply(reader,(q,))
    po.close()
    po.join()
    print("(%s) End"%os.getpid())