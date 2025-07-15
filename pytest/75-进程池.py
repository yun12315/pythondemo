from  multiprocessing import Pool
import os,time,random

# def workder(msg):
#     t_start = time.time()
#     print("%s开始执行,进程号为%d"%(msg,os.getpid()))
#     time.sleep(random.random()*2)
#     t_stop = time.time()
#     print("%s执行完成，耗时%.2f"%(msg,(t_stop-t_start)))
#
#     # for i in range(random.randint(1,3)):
#     #     print("----pid = %d----"%os.getpid())
#
# if __name__ == '__main__':
#     """
#     Windows不使用fork来创建新进程，而是通过spawn方式，这要求所有顶级模块保护被放置在if __name__ == '__main__':之下。
#     Windows操作系统使用spawn方法来启动新的Python解释器进程，而非像Unix/Linux那样使用fork。
#     如果代码中直接在顶层命名空间（全局作用域）中创建了Pool实例或启动了其他多进程操作，那么当新的解释器进程启动时，它会再次执行顶层代码，导致递归地试图创建更多的进程。
#     为了防止这种情况，任何涉及创建新进程的代码都应当放在if __name__ == '__main__':保护块内。
#     """
#     po = Pool(4) # 创建 4 个进程的进程池
#     for i in range(0,10):
#         # Pool.apply_async(要调用的目标,args=(传递给目标的参数元组,))
#         #每次循环将会用空闲出来的子进程去调用目标
#         po.apply_async(workder,(i,))
#
#     print("-----start-----")
#     po.close() # 关闭进程池，关闭后po不再接收新的请求
#     po.join() # 等待po中所有子进程执行完成，再执行下面的代码,必须放在close后面
#     print("-----end-----")


def worker(num):
    for i in range(5):
        print("======pid=%d====num=%d==="%(os.getpid(),num))
        time.sleep(1)

if __name__ == '__main__':
    # 创建进程池，创建的进程数量为3
    pool = Pool(3)
    # 向进程池中添加进程,添加的进程会根据进程池中进程的数量进行分配,如果添加的进程大于进程池中进程的数量,那么就会创建新的进程，不会添加不了
    # 添加到进程中的任务如果还没有被执行的话，他们会等待进程池中的进程完成一个任务后，自动的去用刚刚创建的进程去执行完成当前的新任务
    for i in range(10):
        print("----------%d-------"%i)
        pool.apply_async(worker,(i,)) # apply_async(要调用的目标,args=(传递给目标的参数元组,))，每次循环将会用空闲出来的子进程去调用目标，非阻塞的
        #pool.apply(worker,(i,)) # apply(要调用的目标,args=(传递给目标的参数元组,))，每次循环将会用空闲出来的子进程去调用目标，阻塞的

    pool.close() # 关闭进程池，关闭后po不再接收新的请求，不能再向进程池中添加新的进程，只能等待已经添加的进程执行完成
    pool.join() # 主进程默认不会等待进程池中的任务执行完成后才结束，而是当主进程任务做完后立马结束，如果这里没有join会导致进程池中的任务不会执行，等待po中所有子进程执行完成，再执行下面的代码,必须放在close后面