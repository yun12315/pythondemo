def test(number):
    print("test-----")

    # 闭包
    def test2(number_in):
        print("test2-------")
        return number + number_in

    print("------2------")
    return test2

b = test # b是一个函数的引用
print(b)
print(test)
#test(100)
ret = test(100)
print(ret(150))
print(test(100))