class Test(object):
    def __init__(self):
        self.__num = 100
    # def setNum(self,newNum):
    #     print("----setter----")
    #     self.__num = newNum
    # def getNum(self):
    #     print("----getter----")
    #     return self.__num
    #
    # num = property(getNum,setNum)
    @property
    def num(self):
        print("----getter----")
        return self.__num
    @num.setter
    def num(self,newNum):
        print("----setter----")
        self.__num = newNum

t =  Test()
t.num = 200 # 调用setter方法 t.setNum(200)
print(t.num) # 调用getter方法 t.getNum()
