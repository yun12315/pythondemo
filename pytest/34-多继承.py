class Base(object):
    def test2(self):
        print("Base")

class A(Base):
    def test2(self):
        print("A")
class B(Base):
    def test2(self):
        print("B")
class C(A,B):
    def test2(self):
        print("C")

c = C()
#c.test1()
c.test2()
#c.test()
print(C.__mro__) # 查看类的继承顺序(<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class '__main__.Base'>, <class 'object'>)
