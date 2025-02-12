class Tool(object):  # 类对象
    """工具类"""
    # 类属性 属于所属类对象，多个实例对象共享一个类属性
    count = 0
    # 方法
    def __init__(self, name):
        # 实例属性
        self.name = name
        Tool.count += 1

num = 0
too1 = Tool('hammer') # 实例对象 ，实例属性：和具体的某个实例对象有关系，多个实例对象不可以共享实例属性
num += 1
too2 = Tool('screwdriver')
num += 1
tool3 = Tool('wrench')
print(num)
print(Tool.count)