class Animal:
    def eat(self):
        print("吃东西")
    def sleep(self):
        print("睡觉")

    def drink(self):
        print("喝水")

    def run(self):
        print("跑")

class Dog(Animal):
    def bark(self):
        print("汪汪叫")

class Cat(Animal):
    def catch(self):
        print("抓老鼠")

a = Animal()
a.eat()
b = Dog()
b.bark()
c = Cat()
c.catch()
#c.bark() #AttributeError: 'Cat' object has no attribute 'bark' 不能使用其它子类的方法