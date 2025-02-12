def func(functionName):
    print("------func------1")
    def func_in(*args,**kwargs): #如果a,b没有定义，会导致14行报错
        print("------func_in------1")
        result = functionName(*args,**kwargs)#如果没有把a,b当作参数进行传递，会导致调用10行报错
        print("------func_in------2")
        return result #返回到16行处的调用
    return func_in  # 返回一个函数的引用

@func
def test(a,b,c):
    print("------test----a=%d,b=%d,c=%d--"%(a,b,c))
    return a+b+c
@func
def test2(a,b,c):
    print("------test2----a=%d,b=%d,c=%d--"%(a,b,c))

#test = func(test)
ret = test(1,2,3)
print("test return value is %s"%ret)
print("---------------------------------")
print(test(11,22,33))
print("---------------------------------")
print(test2(22,33,44))