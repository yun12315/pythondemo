def test(a,b,func):
    result = func(a,b)
    return result

func_new = input("请输入一个函数：")
func_new = eval(func_new)

num = test(3,2,func_new)
print(num)