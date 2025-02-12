def test(a,b,func):
    result = func(a,b)
    return result
num = test(3,2,lambda x,y:x*y)
print(num)