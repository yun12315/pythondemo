import types


class Person(object):
    # __slots__ = ("name","age") # 限制class实例能添加的属性
    def __init__(self,newName,newAge):
        self.name = newName
        self.age = newAge
    def eat(self):
        print("%s is eating"%self.name)

def run(self):
    print("%s is running"%self.name)

@staticmethod # 静态方法
def text_analyse(self):
    print("%s is texting"%self.name)
    return "text_analyse"

@classmethod # 类方法
def printNum(cls):
    print("%s is texting？"%cls.name)
    return "text_analyse"

p1 = Person("p1",18)
p1.eat()
#p1.run = run
#p1.run()
"""
虽然p1对象中 run属性已经指向了run方法，
 方法定义问题：如果 run() 方法是在类中定义的实例方法，它应该隐式地接收 self 参数。如果直接通过类名调用而不是实例化对象调用，则不会自动传递 self。
 调用方式问题：如果 p1 是类的实例，但仍然出现此错误，可能是方法定义或调用方式有误。
"""

aa = types.MethodType(run,p1) # 给对象动态添加方法
aa()
p1.text = types.MethodType(text_analyse,p1) # 给对象动态添加静态方法
print(p1.text())

# 动态添加类属性
setattr(Person,"name","李四")
Person.printNum = printNum # 给类动态添加类方法
Person.printNum()

# lawang = Person("lawang",18)
# print(lawang.name)
# print(lawang.age)
# lawang.sex = "男" # 给对象动态添加属性
# print(lawang.sex)
# print(lawang.__dict__)
#
# laozhao = Person("laozhao",18)
# #print(laozhao.sex)
#
# Person.num = 100 # 给类动态添加属性
# print(lawang.num)
# print(laozhao.num)