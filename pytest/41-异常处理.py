import time

try:
    print(a)
    print(1/0)
    print("--------1------------")
except Exception as e:
    print("出错啦")


while True:
    flag = 1 
    time.sleep(1)
    if flag == 1:
        flag = 0
        print("haha")
    if flag == 0:
        print("aaaa")
        break

print("---------2----------")