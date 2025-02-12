a = [1,2,3]
b = a # a和b指向同一个对象 浅拷贝
print(id(a),id(b))

import copy
c = copy.copy(a)
d = copy.deepcopy(a)
print(id(a),id(c),id(d))

a.append(4)
print(a,b,c,d)

e = [1,2,3]
f = [4,5,6]
k = [e,f]
print(k)
g = k
#m = copy.copy(k) # 浅拷贝 可变类型拷贝指向不同的引用
m = copy.deepcopy(k) # 深拷贝 可变类型拷贝指向不同的引用
#print(id(k),id(g))
print(id(k),id(m))
#print(id(k[0]),id(m[0]))
e.append(7)
print(k[0],m[0])


a = [1,2,3]
b = [4,5,6]
c = (a,b)
e = copy.copy(c) # 浅拷贝 指向同一个引用
e = copy.deepcopy(c)# 深拷贝 指向新的引用
a.append(4)
print(c,e)
print(id(c),id(e))

a = [1,2,3]
b = [4,5,6]
c = (a,b)
e = copy.copy(c) # 浅拷贝 不可变类型指向同一个引用
print(id(c),id(e))