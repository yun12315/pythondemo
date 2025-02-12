class Dog(object):
    def print_self(self):
        print("我是小土狗")
class Xiaotq(Dog):
    def print_self(self):
        print("我是哮天犬")

def introduce(temp):
    temp.print_self() # 定义时不确定调用哪个类的print_self()方法

dog1 = Dog()
dog2 = Xiaotq()

introduce(dog1) # 调用时传入的参数是Dog类，所以调用的是Dog类中的print_self()方法
introduce(dog2) # 调用时传入的参数是Xiaotq类，所以调用的是Xiaotq类中的print_self()方法