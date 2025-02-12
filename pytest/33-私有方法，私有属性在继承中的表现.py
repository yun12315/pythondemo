class A:
    def __init__(self):
        self.a = 1
        self._b = 2
        self.__c = 3
    def test1(self):
        print(self.a)
    def __test2(self):
        print(self._b)

    def test3(self):
        self.__test2()
        print(self.__c)
class B(A):
    def test4(self):
        self.__test2()
        print(self.__c)

b = B()
b.test1()
b.test3()
#b.test4() # 如果调用的是继承的父类中的共有方法，可以在这个公有方法中访问父类的私有属性和私有方法，
          # 但是如果调用的是私有方法或属性，则不能在子类中访问，会报错：AttributeError: 'B' object has no attribute '__c'
#b.__test2() # 私有方法不会被继承
#print(b.__c) # 私有属性不会被继承
print(b.a)
print(b._b)