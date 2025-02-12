# 列表与字典全局变量用加global
nums = [1,2,3,4,5,6,7,8,9]
infor = {'name':'zhangsan','age':18,'sex':'男'}

def test1():
    nums.append(10)
    infor['age'] = 20
def test2():
    print(nums)
    print(infor)

test1()
test2()