class Dog(object):
    def __init__(self):
        print("-----init方法------")
    def __del__(self):
        print("----del方法-----")
    def __str__(self):
        return "我是%s,今年%d岁了" % (self.name,self.age)
    def __new__(cls, *args, **kwargs): # cls是Dog指向的类对象
        print("new方法被调用")
        print(id(cls))
        return object.__new__(cls)
    def __call__(self, *args, **kwargs):
        print("call方法被调用")
        print(args)
        print(kwargs)
        return "call方法返回的结果"
print(id(Dog))
xtq = Dog() # 1.调用__new__方法创建对象
            # 2.调用__init__方法初始化对象，然后用一个变量接收__new__方法返回的对象的引用
            # 3.返回对象的引用