# coding=utf-8
import builtins
import pprint

#num = 100 #全局变量没有就找内层变量
def test1():
    a = 100
    b = 200
    #num = 200
    def test2():
        #num = 300
        print(num)
    return test2
    print(locals())
    print("test")

ret = test1()
ret()
pprint.pprint(dir(builtins))