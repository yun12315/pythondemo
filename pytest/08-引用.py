a = 100
b = a

print(id(a))
print(id(b))

A = [1, 2, 3]
B = A

A.append(44)
print(id(A))
print(id(B))
print(A)
print(B)