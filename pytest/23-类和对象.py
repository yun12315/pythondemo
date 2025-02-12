class Student:
    # 类属性
    school = '北京邮电大学'
    def __init__(self, name, age):
        # 实例属性
        self.name = name
        self.age = age
        #print(self.name)

    def __str__(self):
        return '我是%s,今年%d岁' % (self.name,self.age)
    def study(self):
        print('%s正在学习' % self.name+",年龄："+str(self.age))

#创建一个对象
s1 = Student(name='lisi',age=19)
print(s1)
#s1.name="zhangshan"
#s1.age=18
#s1.study()

s2 = Student(name='wangwu',age=20)
print(s2)