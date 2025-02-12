
__all__ = ['sendmsg', 'recvmsg'] # 指定模块中哪些函数被导入

def sendmsg(msg):
    print("send msg:", msg)
def recvmsg(size):
    print("recv msg:", size)

num = 100

class Test(object):
    def __init__(self, name):
        self.name = name