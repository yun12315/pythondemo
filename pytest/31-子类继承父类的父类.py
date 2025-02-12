class Animal:
    def eat(self):
        print("吃吃吃")
    def drink(self):
        print("喝喝喝")
    def sleep(self):
        print("睡觉")
    def run(self):
        print("跑跑跑")

class Dog(Animal):
    def bark(self):
        print("汪汪汪")

class Xiaotq(Dog):
    def fly(self):
        print("飞飞飞")

xiaotq = Xiaotq()
xiaotq.fly()
xiaotq.bark()
xiaotq.eat()