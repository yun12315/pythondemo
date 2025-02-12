a = [i for i in range(10) ]
print(a)
b = [11 for i in range(10)]
print(b)
c = [i for i in range(10) if i%2==0]
print(c)
d = [i for i in range(10) if i%2==0 for j in range(10) if j%2==1]
print(d)
e = [(i,j) for i in range(10) for j in range(10)]
print(e)
f = [(i,j,k) for i in range(10) for j in range(10) for k in range(10)]
print(f)