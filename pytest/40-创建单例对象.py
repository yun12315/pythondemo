class Singleton(object):
    __instance = None
    def __new__(cls, name,*args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance
    def __init__(self,name):
        # 只有在属性未设置时才设置名字
        if not hasattr(self, 'name'):
            self.name = name
            print("初始化")

a = Singleton("旺财")
print(id(a))
print(a.name)
b = Singleton("小黑")
print(id(b))
print(b.name)