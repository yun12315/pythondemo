a = [x*2 for x in range(10)]
print(a)
b = (x*2 for x in range(10) if x%2==0)
print(b)
for i in b:
    #print(next(b)) #b是生成器，不能重复遍历
    print(i)
print("----------")
def creatNum():
    """
    生成器函数
    """
    print("-------------start-----------")
    a,b = 0,1
    while a < 5:
        print("----------1-----------")
        yield b #yield返回值，生成器
        print("---b---",b)
        a,b = b,a+b
        print("----------2-----------")
    print("-------------end-----------")

a = creatNum()
print(a)
# for v in range(10):
#     print(next(a))
# print("-----xxxxxxxxxxxxxxxxxxxx-----")
# for i in a:
#     print(i)

ret = a.__next__()
print(ret)
print("-----zzzzzzzzzzzzzzzzzzz-----")
def fib(n):
    """
    生成器函数
    """
    a,b = 0,1
    while a < n:
        yield b
        a,b = b,a+b

for i in fib(10):
    print(i)

def test():
    i = 0
    while i<5:
        temp = yield i #
        print("temp:",temp)
        i += 1

t = test()
for i in range(5):
    #print(t.__next__())
    #print(t.send("haha"))
    print(t.send(None))

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
def test():
    i = 0
    while i<5:
        if i ==0:
            temp = yield i
        else:
            yield i
        i+=1
t = test()
print(t.__next__())
print("$$$$$$$$$$$$$$$$$$$")
# for i in range(5):
#     print(t.send("haha"))

# 死循环,多任务，协程
def test1():
    while True:
        print("-----1----")
        yield None
def test2():
    while True:
        print("-----2----")
        yield None

t1 = test1()
t2 = test2()
while True:
    print("-----3----")
    t1.__next__()
    t2.__next__()
