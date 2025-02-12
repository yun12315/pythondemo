
def func_arg(arg):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print('----记录日志---arg=%s----'%arg)
            if arg == "haha":
                func(*args,**kwargs)
                print('----test----' )
            else:
                func(*args, **kwargs)
            return func(*args, **kwargs)
        return wrapper
    return decorator
#1. 先执行func_arg("haha")函数，，这个函数return 的结果是decorator这个函数的引用
#2. @decorator
#3. 使用@decorator对test进行装饰
@func_arg("haha")
def func(a, b):
    print(a, b)
    return a + b
# 带参数的装饰器能起到在运行时执行不同的功能
@func_arg("heihei")
def func2(a, b):
    print(a, b)
    return a + b

#func(1, 2)
func2(1, 2)