import os as tt
from mymodule.myfirstmodule import greeting,sendmsg
from mymodule.myfirstmodule import *
from mymodule.sendmsg import * # 不同模块里面的相同方法会被后面导入的模块里面的方法覆盖
from mymodule.recvmsg import *

print(tt.__file__)

def get_path(path):
    return tt.path.abspath(path)

sendmsg("tom")
greeting("John")
recvmsg(sendmsg("hello"),1)