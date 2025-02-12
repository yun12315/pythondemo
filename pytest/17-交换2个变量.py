# a =4
# b = 5
# c = a
# a = b
# b = c
# print("a=%d,b=%d"%(a,b))

# a = a + b
# b = a - b
# a = a - b
# print("a=%d,b=%d"%(a,b))

# a,b = b,a
# print("a=%d,b=%d"%(a,b))
a =100
#a = [100]

def test(num):
    num += num # a =100 不可修改，定义了新的变量num,所以num和a不是同一个对象 a = [100]可修改，因为是引用，所以num和a是同一个对象
    print(num)

test(a)
print(a)