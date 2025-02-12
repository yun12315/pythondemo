# 装饰器
# 函数作为参数 调用时从上到下执行，装饰时从下到上执行
def w1(func):
    print("---正在装饰---")
    def inner():
        print("---权限验证----")
        if False:
            print("---权限验证通过----")
            func()
        else:
            print("---权限验证失败----")
    return inner

# 只要python解释器遇到@w1，就自动执行w1函数，并将w1返回的函数赋值给f1,而不是等到函数调用的时候才执行w1函数
@w1  #f1 = w1(f1) 执行了
def f1():
    print("f1")

@w1
def f2():
    print("f2")

#innerFunc = w1(f1)
#innerFunc()

#f1 = w1(f1)
#f1()
#在调用f1之前,f1被w1装饰过
#f1()
#f2()