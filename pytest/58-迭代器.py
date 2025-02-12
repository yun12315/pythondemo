from collections.abc import Iterable

a = [1, 2, 3, 4, 5]
print(type(a))

b = iter(a) # 把a转成迭代器 ，迭代器是一个可迭代对象，占用空间少
print(type(b))
print(isinstance(a, Iterable))
print(isinstance(b, Iterable))
#print(isinstance(next(a), Iterable)) # 不可迭代
print(isinstance((x for x in a), Iterable))
print(isinstance(100, Iterable))
