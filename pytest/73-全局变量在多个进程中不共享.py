import os
import time

g_num = 100

ret = os.fork()

if ret == 0:
    print("----子进程----")
    g_num += 1
    print("g_num=%d"%g_num)
else:
    print("----父进程----")
    print("g_num=%d"%g_num)
    time.sleep(3)
    print("g_num=%d"%g_num)