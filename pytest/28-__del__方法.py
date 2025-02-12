class Dog:

    def __del__(self):
        print("对象被销毁了")

dog1 = Dog()
dog2 = dog1

del dog1
#del dog2
print("=========================")