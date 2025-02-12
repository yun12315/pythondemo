a = "hello"
#a[0]="bb" # TypeError: 'str' object does not support item assignment
print(a[0])

b = 11
#b[0] = 22 # TypeError: 'int' object does not support item assignment
print(b)

c = (1,2)
#c[0]="asdf" # TypeError: 'tuple' object does not support item assignment
print(c)

d = [1,2]
d[0] = 3 # 列表可修改
print(d)

e = {"name":"laowang","age":18}
e["name"]="zhaoshan" # 字典可修改
print(e)

infor = {"name":"laowang","age":18,3.14:"pi"}
infor = {(11,22):"hello"}
infor = {[11,22]:"world"}# TypeError: unhashable type: 'list' 列表不可作为字典的key
