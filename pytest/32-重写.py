class Animal:
    def eat(self):
        print("吃")
    def drink(self):
        print("喝")
    def run(self):
        print("跑")
    def sleep(self):
        print("睡")

class Dog(Animal):
    def bark(self):
        print("叫")
class XiaoTianQuan(Dog):
    def fly(self):
        print("飞")

    # 重写
    def bark(self):
        print("-----狂吠-----")
        Dog.bark(self) # 调用父类的方法
        #super().bark() # 调用父类的方法

xiaotq = XiaoTianQuan()
xiaotq.fly()
xiaotq.bark()
xiaotq.eat()