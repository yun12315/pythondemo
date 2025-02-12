from multiprocessing import Process
import time
import os

#继承Process类
class MyProcess(Process):
    def __init__(self,interval):
        super(MyProcess,self).__init__()
        self.interval = interval

    # 重写Process类的run方法
    def run(self):
        print('子进程%s开始执行，父进程为%s'%(os.getpid(),os.getppid()))
        t_start = time.time()
        time.sleep(self.interval)
        t_stop = time.time()
        print('子进程%s执行结束，耗时%.03f秒'%(os.getpid(),(t_stop-t_start)))

if __name__=="__main__":
    t_start = time.time()
    print('Parent process %s.' % os.getpid())
    p = MyProcess(2)
    print('Child process will start.')
    p.start()
    p.join()
    t_stop = time.time()
    print('Child process end.')