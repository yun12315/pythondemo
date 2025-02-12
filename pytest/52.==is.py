a = [11,22,33]
b = a
c = [11,22,33]
print("a的地址："+str(id(a)))
print("b的地址："+str(id(b)))
print("c的地址："+str(id(c)))
print(a is b)
print(a is c)
print(a == b)
print(a == c)

a = 100
b = 100
print(a==b)
print(a is b)

a = 10000
b = 10000
print(a==b)
print(a is b)