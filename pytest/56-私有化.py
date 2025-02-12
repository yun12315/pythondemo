class Test(object):
    def __init__(self):
        self.__num = 100
    def setNum(self,newNum):
        self.__num = newNum
    def getNum(self):
        return self.__num
    """
    私有变量：
        1. __开头
        2. 不能直接访问，只能通过getter和setter方法访问
        3. 不能在类外部直接访问，只能通过getter和setter方法访问
        4. 在类内部可以访问，在类外部不能访问
        5. _x:单前置下划线，私有化属性或方法，from somemodule import * 禁止导入，类对象和子类可以访问
        6. __xx:双前置下划线，避免与子类中的属性名冲突，无法在外部直接访问（名字重整所以访问不到)
        7.__xx__:双前后下划线，用户名字空间的魔法对象或属性。例如：__init__,__不要自己发明这样的名字
        8.xx_:单后置下划线，用于避免与Python关键词的冲突
    """
t = Test()
#t.__num = 200 # 给t对象添加一个私有变量__num
#print(t.__num)
#t.__num = 200 # __num是私有变量，不能直接访问，只能通过getter和setter方法访问
print(t.getNum())
t.setNum(500)
print(t.getNum())