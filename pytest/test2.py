import gc
class ClassA():
    def __init__(self):
        print('object born,id:%s'%str(hex(id(self))))

def f2():
    i = 0
    while i < 3:
        i += 1
        c1 = ClassA()
        c2 = ClassA()
        c1.t = c2
        c2.t = c1
        del c1
        del c2
        gc.collect()

gc.disable()

f2()