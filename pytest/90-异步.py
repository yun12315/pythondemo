from multiprocessing import Pool, freeze_support
import os,time

def test():
    print("---进程池中的进程---pid=%d,ppid=%d-----"%(os.getpid(),os.getppid()))
    for i in range(10):
        print("---in test1--%d-"%i)
        time.sleep(1)
    return "haha"

def test2(args):
    print("---callback---pid=%d,ppid=%d-----"%(os.getpid(),os.getppid()))
    print("---in test2--%s-"%args)

if __name__ == '__main__':
    freeze_support()
    pool = Pool(3)
    pool.apply_async(func=test,callback=test2)
    while True:
        time.sleep(1)
        print("----主进程-pid=%d-----"%os.getpid())
    pool.close()
    pool.join()
    print("----主进程-pid=%d-----"%os.getpid())