import multiprocessing
import time
import os

def child_process():
    while True:
        print(f"子进程: PID={os.getpid()}, 父进程PID={os.getppid()}")
        time.sleep(1)

def worker(num):
    """子进程要执行的函数"""
    print(f'Worker: {num}')

def square(x):
    return x * x

if __name__ == "__main__":
    # 创建子进程并启动
    p = multiprocessing.Process(target=child_process)
    processes = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()  # 等待所有子进程完成
    #p = os.fork() # fork()函数创建子进程,用于linux系统  p>0 父进程执行

    with multiprocessing.Pool(processes=4) as pool:  # 创建 4 个进程的进程池
        results = pool.map(square, range(10))  # 将 square 函数应用于 range(10)
        print(results)  # 输出 [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

    try:
        while True:
            print(f"父进程: PID={os.getpid()}, 父进程PID={os.getppid()}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("父进程收到中断信号，正在终止子进程...")
        p.terminate()
        p.join()
        print("子进程已终止")


